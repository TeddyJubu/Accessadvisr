# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Listing, Review, Category, ListingPhoto, TeamMember, Partner, ContactMessage, BlogCategory, BlogPost, SponsorshipPackage, DonationGoal
from .forms import ReviewForm, ListingSubmissionForm, ListingPhotoForm, ContactForm
from .utils import geocode_listing
from .emails import (
    send_review_submitted_email,
    send_review_approved_email,
    send_welcome_email,
    send_listing_approved_email,
)


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
    features = request.GET.getlist("features")  # Multiple accessibility features
    
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q))
    if category and category != "all":
        qs = qs.filter(categories__icontains=category)
    if location:
        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))
    if status and status != "all":
        qs = qs.filter(status=status)
    
    # Filter by accessibility features (AND logic - must have ALL selected features)
    for feature in features:
        if feature:
            qs = qs.filter(accessibility_features__icontains=feature)
    
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
        "selected_features": features,
    })


def listing_detail(request, pk):
    """Detail page for a single listing"""
    listing = get_object_or_404(Listing, pk=pk, moderation_status="approved")
    reviews = listing.reviews.filter(moderation_status="approved")
    badges = listing.get_accessibility_badges()
    photos = listing.get_all_photos()
    
    # Initialize review form
    review_form = ReviewForm()
    
    return render(request, "core/listing_detail.html", {
        "listing": listing,
        "reviews": reviews,
        "badges": badges,
        "photos": photos,
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
        
        # Send confirmation email if user provided email
        send_review_submitted_email(review)
        
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
            
            # Send approval notification emails
            if item_type == "review":
                send_review_approved_email(item)
            elif item_type == "listing":
                # For listings, we don't have submitter email stored yet
                # This can be enhanced when we add user-owned listings
                pass
            
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
    features = request.GET.getlist("features")  # Multiple accessibility features
    
    # Only return approved listings
    qs = Listing.objects.filter(moderation_status="approved")
    
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q) | Q(description__icontains=q))
    if category and category not in ("Filter by category", "all", ""):
        qs = qs.filter(categories__icontains=category)
    if location:
        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))
    if status and status != "all":
        qs = qs.filter(status=status)
    
    # Filter by accessibility features (AND logic - must have ALL selected features)
    for feature in features:
        if feature:
            qs = qs.filter(accessibility_features__icontains=feature)
    
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
    
    return JsonResponse({"listings": data, "count": len(data), "filters": {"features": features}})


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Send welcome email
            send_welcome_email(user)
            
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


# =============================================================================
# PHOTO MANAGEMENT VIEWS
# =============================================================================

@require_POST
def upload_photos(request, pk):
    """Handle photo uploads for a listing"""
    listing = get_object_or_404(Listing, pk=pk)
    
    # Handle multiple file uploads
    files = request.FILES.getlist('photos')
    
    if not files:
        messages.error(request, "No photos selected.")
        return redirect('listing_detail', pk=pk)
    
    uploaded_count = 0
    for photo_file in files:
        # Create ListingPhoto for each uploaded file
        photo = ListingPhoto(
            listing=listing,
            image=photo_file,
            caption=photo_file.name.rsplit('.', 1)[0][:100],  # Use filename as caption
        )
        
        # If this is the first photo, make it primary
        if not listing.listing_photos.exists():
            photo.is_primary = True
        
        photo.save()
        uploaded_count += 1
    
    if uploaded_count > 0:
        messages.success(request, f"Successfully uploaded {uploaded_count} photo(s).")
    
    return redirect('listing_detail', pk=pk)


@require_POST
def delete_photo(request, pk, photo_id):
    """Delete a photo from a listing"""
    listing = get_object_or_404(Listing, pk=pk)
    photo = get_object_or_404(ListingPhoto, pk=photo_id, listing=listing)
    
    was_primary = photo.is_primary
    photo.delete()
    
    # If we deleted the primary photo, set the next one as primary
    if was_primary:
        next_photo = listing.listing_photos.first()
        if next_photo:
            next_photo.is_primary = True
            next_photo.save()
    
    messages.success(request, "Photo deleted.")
    return redirect('listing_detail', pk=pk)



@require_POST
def set_primary_photo(request, pk, photo_id):
    """Set a photo as the primary photo for a listing"""
    listing = get_object_or_404(Listing, pk=pk)
    photo = get_object_or_404(ListingPhoto, pk=photo_id, listing=listing)
    
    # Setting is_primary will automatically unset others (via model save method)
    photo.is_primary = True
    photo.save()
    
    messages.success(request, "Primary photo updated.")
    return redirect('listing_detail', pk=pk)


def about(request):
    """About Us and Accessibility Statement page"""
    team_members = TeamMember.objects.filter(is_active=True)
    return render(request, "core/about.html", {"team_members": team_members})


def partners(request):
    """Sponsors and Partners page"""
    sponsors = Partner.objects.filter(type="sponsor", is_active=True)
    partners = Partner.objects.filter(type="partner", is_active=True)
    return render(request, "core/partners.html", {
        "sponsors": sponsors,
        "partners": partners,
    })


def contact(request):
    """View for handling the Contact Us page"""
    from django.conf import settings
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            messages.success(request, "Your message has been sent successfully! We'll get back to you soon.")
            
            # Optional: send email notification
            try:
                from django.core.mail import send_mail
                send_mail(
                    subject=f"New Contact Form Submission: {contact_msg.subject}",
                    message=f"From: {contact_msg.name} <{contact_msg.email}>\n\n{contact_msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
                
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_BROWSER_KEY,
    }
    return render(request, 'core/contact.html', context)


def blog_list(request):
    """Paginated list of blog posts"""
    category_slug = request.GET.get('category')
    posts = BlogPost.objects.filter(is_published=True)
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = BlogCategory.objects.all()
    
    return render(request, 'core/blog_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
    })


def blog_detail(request, slug):
    """Full article view"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    categories = BlogCategory.objects.all()
    
    return render(request, 'core/blog_detail.html', {
        'post': post,
        'recent_posts': recent_posts,
        'categories': categories,
    })


def packages(request):
    """Sponsorship packages page"""
    import logging
    logger = logging.getLogger(__name__)
    try:
        packages = SponsorshipPackage.objects.filter(is_active=True).order_by('order')
        return render(request, 'core/packages.html', {'packages': packages})
    except Exception as e:
        logger.error(f"Error in packages view: {e}", exc_info=True)
        raise


def donate(request):
    """Donation goals and fundraiser page"""
    goals = DonationGoal.objects.filter(is_active=True)
    return render(request, 'core/donate.html', {'goals': goals})
