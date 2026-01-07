# core/models.py
from django.db import models
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
    description = models.TextField(blank=True)
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
