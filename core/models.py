# core/models.py
from django.db import models
from tinymce.models import HTMLField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Category for listings with marker styling"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="map-pin")  # Lucide icon name
    color = models.CharField(max_length=7, default="#FF431E")  # Hex color for markers

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Listing(models.Model):
    """Accessible venue listing"""
    MODERATION_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("temporarily_closed", "Temporarily Closed"),
    ]

    # Basic info
    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = HTMLField(blank=True)
    categories = models.JSONField(default=list)  # ["Food & Restaurants", "Sport"]
    
    # Location
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    
    # Contact
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    
    # Business details
    price_min = models.IntegerField(null=True, blank=True)
    price_max = models.IntegerField(null=True, blank=True)
    opening_hours = models.JSONField(default=dict)  # {"mon": "9:00-17:00", ...}
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    
    # Media
    photos = models.JSONField(default=list)  # List of photo URLs
    
    # Accessibility features (quick tags)
    accessibility_features = models.JSONField(default=list)  # ["wheelchair", "braille", ...]
    
    # Ratings (auto-computed from reviews)
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    
    # Metadata
    tags = models.JSONField(default=list)
    featured = models.BooleanField(default=False)
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES, default="approved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-rating", "name"]

    def location_text(self):
        return f"{self.city}, {self.country}"

    def __str__(self):
        return self.name

    def get_accessibility_badges(self):
        """Compute accessibility badges from approved reviews"""
        reviews = self.reviews.filter(moderation_status="approved")
        if not reviews.exists():
            return []
        
        badges = []
        thresholds = {
            "step_free_access": ("Step-Free Access", "wheelchair"),
            "restroom_accessible": ("Accessible Restroom", "accessibility"),
            "signage_clear": ("Clear Signage", "signpost"),
            "staff_supportive": ("Helpful Staff", "heart-handshake"),
            "sensory_friendly": ("Sensory Friendly", "ear"),
        }
        
        for field, (label, icon) in thresholds.items():
            avg = reviews.exclude(**{field: None}).aggregate(avg=Avg(field))["avg"]
            if avg and avg >= 4.0:  # 80%+ positive (4+ out of 5)
                badges.append({"label": label, "icon": icon})
        
        return badges

    def get_primary_photo(self):
        """Get the primary photo or first uploaded photo"""
        primary = self.listing_photos.filter(is_primary=True).first()
        if primary:
            return primary
        return self.listing_photos.first()
    
    def get_all_photos(self):
        """Get all photos for this listing, primary first"""
        return self.listing_photos.all().order_by('-is_primary', '-uploaded_at')
    
    @property
    def has_photos(self):
        """Check if listing has any uploaded photos"""
        return self.listing_photos.exists()


def listing_photo_path(instance, filename):
    """Generate upload path: listings/<listing_id>/<filename>"""
    import os
    import uuid
    ext = filename.split('.')[-1].lower()
    new_filename = f"{uuid.uuid4().hex[:12]}.{ext}"
    return f"listings/{instance.listing.id}/{new_filename}"


class ListingPhoto(models.Model):
    """Photo uploaded for a listing"""
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='listing_photos'
    )
    image = models.ImageField(upload_to=listing_photo_path)
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Description for screen readers"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Primary photo shown in listings and map"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = "Listing Photo"
        verbose_name_plural = "Listing Photos"
    
    def __str__(self):
        return f"Photo for {self.listing.name}"
    
    def save(self, *args, **kwargs):
        # If this is marked as primary, unset other primaries for this listing
        if self.is_primary:
            ListingPhoto.objects.filter(
                listing=self.listing, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    
    @property
    def url(self):
        """Get the URL for the image"""
        if self.image:
            return self.image.url
        return None


class Review(models.Model):
    """User review with accessibility-focused fields"""
    MODERATION_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)  # Optional, for moderation contact
    
    # Overall rating
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    
    # Accessibility checklist (1-5 scale, optional)
    step_free_access = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Poor, 5=Excellent"
    )
    restroom_accessible = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Poor, 5=Excellent"
    )
    signage_clear = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Poor, 5=Excellent"
    )
    staff_supportive = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Poor, 5=Excellent"
    )
    sensory_friendly = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Poor, 5=Excellent (lighting, noise, etc.)"
    )
    
    # Metadata
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} - {self.listing.name} ({self.rating}★)"


# Signals to auto-update listing ratings when reviews change
@receiver(post_save, sender=Review)
def update_listing_rating_on_save(sender, instance, **kwargs):
    """Recalculate listing rating when a review is saved"""
    listing = instance.listing
    approved_reviews = listing.reviews.filter(moderation_status="approved")
    avg_rating = approved_reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    listing.rating = round(avg_rating, 1)
    listing.reviews_count = approved_reviews.count()
    listing.save(update_fields=["rating", "reviews_count"])


@receiver(post_delete, sender=Review)
def update_listing_rating_on_delete(sender, instance, **kwargs):
    """Recalculate listing rating when a review is deleted"""
    listing = instance.listing
    approved_reviews = listing.reviews.filter(moderation_status="approved")
    avg_rating = approved_reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    listing.rating = round(avg_rating, 1)
    listing.reviews_count = approved_reviews.count()
    listing.save(update_fields=["rating", "reviews_count"])

class TeamMember(models.Model):
    """Team member profile for About Us page"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = HTMLField()
    photo = models.ImageField(upload_to='team/', null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"


class Partner(models.Model):
    """Partner or Sponsor for AccessAdvisr"""
    PARTNER_TYPES = [
        ("sponsor", "Sponsor"),
        ("partner", "Partner & Friend"),
    ]
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=PARTNER_TYPES, default="partner")
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)
    description = HTMLField(blank=True)
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['type', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class ContactMessage(models.Model):
    """Stores inquiries from the Contact Us page"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, default="Inquiry from Website")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class BlogCategory(models.Model):
    """Categories for blog posts"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Articles, news, and travel guides"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    author = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    content = HTMLField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    meta_description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SponsorshipPackage(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=50, default="Yearly")
    subheading = models.CharField(max_length=500, blank=True)
    features = models.JSONField(help_text="Enter features as a list of strings")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class DonationGoal(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = HTMLField()
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
