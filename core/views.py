# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Listing, Review, Category
from .forms import ReviewForm, ListingSubmissionForm


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
            messages.success(request, "Thank you for your submission! It will be reviewed by our team.")
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


@require_http_methods(["GET", "POST"])
def admin_page(request):
    if request.method == "POST":
        return redirect("admin_page")
    return render(request, "core/admin.html")


@cache_page(60)
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

