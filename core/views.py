# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Review, Category
from .forms import ReviewForm, ListingSubmissionForm
from .utils import geocode_listing


def home(request):
    """Homepage with map and featured listings"""
    featured = Listing.objects.filter(featured=True, moderation_status="approved")[:6]
    recent_reviews = Review.objects.filter(moderation_status="approved").select_related("listing")[:5]
    return render(request, "core/home.html", {
        "featured_listings": featured,
        "recent_reviews": recent_reviews,
    })


def listings_list(request):
    """Public paginated list of approved listings"""
    qs = Listing.objects.filter(moderation_status="approved")
    
    # Apply filters from query params
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    location = request.GET.get("location", "").strip()
    status = request.GET.get("status", "").strip()
    
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q))
    if category and category != "all":
        qs = qs.filter(categories__icontains=category)
    if location:
        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))
    if status and status != "all":
        qs = qs.filter(status=status)
    
    # Pagination
    paginator = Paginator(qs, 12)
    page = request.GET.get("page", 1)
    listings = paginator.get_page(page)
    
    # Get categories for filter dropdown
    categories = Category.objects.all()
    
    return render(request, "core/listings_list.html", {
        "listings": listings,
        "categories": categories,
        "query": q,
        "selected_category": category,
        "selected_location": location,
        "selected_status": status,
    })


def listing_detail(request, pk):
    """Detail page for a single listing"""
    listing = get_object_or_404(Listing, pk=pk, moderation_status="approved")
    reviews = listing.reviews.filter(moderation_status="approved")
    badges = listing.get_accessibility_badges()
    
    # Initialize review form
    review_form = ReviewForm()
    
    return render(request, "core/listing_detail.html", {
        "listing": listing,
        "reviews": reviews,
        "badges": badges,
        "review_form": review_form,
    })


@require_http_methods(["POST"])
def submit_review(request, pk):
    """Handle review form submission"""
    listing = get_object_or_404(Listing, pk=pk, moderation_status="approved")
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.listing = listing
        review.moderation_status = "pending"  # Goes to moderation queue
        review.save()
        messages.success(request, "Thank you for your review! It will be visible after moderation.")
        return redirect("review_success", pk=pk)
    
    # If form invalid, re-render detail page with errors
    reviews = listing.reviews.filter(moderation_status="approved")
    badges = listing.get_accessibility_badges()
    messages.error(request, "Please correct the errors below.")
    
    return render(request, "core/listing_detail.html", {
        "listing": listing,
        "reviews": reviews,
        "badges": badges,
        "review_form": form,
    })


def review_success(request, pk):
    """Success page after submitting a review"""
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "core/review_success.html", {
        "listing": listing,
    })


@require_http_methods(["GET", "POST"])
def submit_listing(request):
    """Form for users to suggest new accessible venues"""
    if request.method == "POST":
        form = ListingSubmissionForm(request.POST)
        if form.is_valid():
            listing = form.save()
            
            # Auto-geocode the new listing
            geocode_success = geocode_listing(listing)
            if geocode_success:
                messages.success(
                    request, 
                    "Thank you! Your venue has been submitted and mapped. It will be reviewed by our team."
                )
            else:
                messages.success(
                    request, 
                    "Thank you for your submission! It will be reviewed and mapped by our team."
                )
            
            return redirect("listing_submission_success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ListingSubmissionForm()
    
    categories = Category.objects.all()
    
    return render(request, "core/submit_listing.html", {
        "form": form,
        "categories": categories,
    })


def listing_submission_success(request):
    """Success page after submitting a new listing"""
    return render(request, "core/listing_submission_success.html")


def admin_page(request):
    """Admin dashboard with moderation queue"""
    # Stats
    stats = {
        "total_listings": Listing.objects.filter(moderation_status="approved").count(),
        "pending_listings": Listing.objects.filter(moderation_status="pending").count(),
        "total_reviews": Review.objects.filter(moderation_status="approved").count(),
        "pending_reviews": Review.objects.filter(moderation_status="pending").count(),
    }
    
    # Pending items for moderation
    pending_listings = Listing.objects.filter(moderation_status="pending").order_by("-created_at")[:10]
    pending_reviews = Review.objects.filter(moderation_status="pending").select_related("listing").order_by("-created_at")[:10]
    
    # Recent approved content
    recent_listings = Listing.objects.filter(moderation_status="approved").order_by("-created_at")[:5]
    recent_reviews = Review.objects.filter(moderation_status="approved").select_related("listing").order_by("-created_at")[:5]
    
    return render(request, "core/admin.html", {
        "stats": stats,
        "pending_listings": pending_listings,
        "pending_reviews": pending_reviews,
        "recent_listings": recent_listings,
        "recent_reviews": recent_reviews,
    })


@require_http_methods(["POST"])
def admin_moderate(request):
    """Handle approve/reject actions from admin dashboard"""
    item_type = request.POST.get("type")
    item_id = request.POST.get("id")
    action = request.POST.get("action")
    
    if not all([item_type, item_id, action]):
        messages.error(request, "Invalid request.")
        return redirect("admin_page")
    
    try:
        if item_type == "listing":
            item = Listing.objects.get(pk=item_id)
            item_name = item.name
        elif item_type == "review":
            item = Review.objects.get(pk=item_id)
            item_name = f"Review by {item.author_name}"
        else:
            messages.error(request, "Invalid item type.")
            return redirect("admin_page")
        
        if action == "approve":
            item.moderation_status = "approved"
            item.save()
            
            # Auto-geocode listings when approved (if missing coordinates)
            if item_type == "listing" and (item.lat is None or item.lng is None):
                if geocode_listing(item):
                    messages.success(request, f"✓ Approved & Geocoded: {item_name}")
                else:
                    messages.success(request, f"✓ Approved: {item_name} (geocoding pending)")
            else:
                messages.success(request, f"✓ Approved: {item_name}")
        elif action == "reject":
            item.moderation_status = "rejected"
            item.save()
            messages.warning(request, f"✗ Rejected: {item_name}")
        else:
            messages.error(request, "Invalid action.")
    except (Listing.DoesNotExist, Review.DoesNotExist):
        messages.error(request, "Item not found.")
    
    return redirect("admin_page")


def listings_api(request):
    """API endpoint for listings with filtering"""
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    location = request.GET.get("location", "").strip()
    status = request.GET.get("status", "").strip()
    
    # Only return approved listings
    qs = Listing.objects.filter(moderation_status="approved")
    
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q))
    if category and category not in ("Filter by category", "all"):
        qs = qs.filter(categories__icontains=category)
    if location:
        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))
    if status and status != "all":
        qs = qs.filter(status=status)
    
    data = [{
        "id": l.id,
        "name": l.name,
        "subtitle": l.subtitle,
        "description": l.description[:200] if l.description else "",
        "categories": l.categories,
        "city": l.city, 
        "country": l.country,
        "address": l.address,
        "phone": l.phone,
        "website": l.website,
        "priceMin": l.price_min, 
        "priceMax": l.price_max,
        "rating": l.rating, 
        "status": l.status,
        "reviewsCount": l.reviews_count,
        "lat": l.lat, 
        "lng": l.lng,
        "accessibilityFeatures": l.accessibility_features,
    } for l in qs if l.lat is not None and l.lng is not None]
    
    return JsonResponse({"listings": data, "count": len(data)})


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to AccessAdvisr, {user.username}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """User profile page"""
    user_reviews = Review.objects.filter(author_name=request.user.username).select_related('listing')
    
    return render(request, 'registration/profile.html', {
        'user_reviews': user_reviews,
    })
