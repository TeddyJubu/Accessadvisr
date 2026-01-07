# core/admin.py
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Category, Listing, Review, ListingPhoto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 1
    fields = ('image', 'caption', 'is_primary', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("author_name", "rating", "comment", "created_at")
    fields = ("author_name", "rating", "moderation_status", "created_at")
    can_delete = False
    show_change_link = True


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "name", "city", "country", "rating", "reviews_count",
        "status", "moderation_status", "has_coordinates", "photo_count"
    )
    list_filter = ("status", "moderation_status", "featured", "country")
    search_fields = ("name", "city", "country", "address")
    readonly_fields = ("rating", "reviews_count", "created_at", "updated_at")
    list_editable = ("moderation_status",)
    inlines = [ListingPhotoInline, ReviewInline]
    actions = ["approve_listings", "reject_listings", "geocode_selected"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "subtitle", "description", "status", "featured", "moderation_status")
        }),
        ("Location", {
            "fields": ("address", "city", "country", "lat", "lng")
        }),
        ("Contact", {
            "fields": ("phone", "email", "website")
        }),
        ("Details", {
            "fields": ("categories", "tags", "price_min", "price_max", "opening_hours")
        }),
        ("Media & Accessibility", {
            "fields": ("photos", "accessibility_features")
        }),
        ("Ratings (Auto-computed)", {
            "fields": ("rating", "reviews_count"),
            "classes": ("collapse",)
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def has_coordinates(self, obj):
        return obj.lat is not None and obj.lng is not None
    has_coordinates.boolean = True
    has_coordinates.short_description = "Geocoded"
    
    def photo_count(self, obj):
        count = obj.listing_photos.count()
        return count if count > 0 else '-'
    photo_count.short_description = "Photos"

    @admin.action(description="Approve selected listings")
    def approve_listings(self, request, queryset):
        updated = queryset.update(moderation_status="approved")
        self.message_user(request, f"{updated} listing(s) approved.", messages.SUCCESS)

    @admin.action(description="Reject selected listings")
    def reject_listings(self, request, queryset):
        updated = queryset.update(moderation_status="rejected")
        self.message_user(request, f"{updated} listing(s) rejected.", messages.WARNING)

    @admin.action(description="Geocode selected listings (requires API)")
    def geocode_selected(self, request, queryset):
        # Filter to only listings missing coordinates
        missing = queryset.filter(lat__isnull=True) | queryset.filter(lng__isnull=True)
        if not missing.exists():
            self.message_user(request, "All selected listings already have coordinates.", messages.INFO)
            return
        # TODO: Implement geocoding via Google API
        self.message_user(
            request,
            f"{missing.count()} listing(s) need geocoding. Run 'python manage.py geocode_listings' to process.",
            messages.WARNING
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "listing", "author_name", "rating", "moderation_status", "created_at"
    )
    list_filter = ("moderation_status", "rating")
    search_fields = ("author_name", "listing__name", "comment")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("moderation_status",)
    actions = ["approve_reviews", "reject_reviews"]

    fieldsets = (
        ("Review", {
            "fields": ("listing", "author_name", "author_email", "rating", "comment", "moderation_status")
        }),
        ("Accessibility Ratings", {
            "fields": ("step_free_access", "restroom_accessible", "signage_clear", "staff_supportive", "sensory_friendly")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        updated = queryset.update(moderation_status="approved")
        # Trigger rating recalculation for affected listings
        for review in queryset:
            review.save()  # This triggers the signal
        self.message_user(request, f"{updated} review(s) approved.", messages.SUCCESS)

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        updated = queryset.update(moderation_status="rejected")
        for review in queryset:
            review.save()
        self.message_user(request, f"{updated} review(s) rejected.", messages.WARNING)


@admin.register(ListingPhoto)
class ListingPhotoAdmin(admin.ModelAdmin):
    list_display = ("listing", "caption", "is_primary", "image_preview", "uploaded_at")
    list_filter = ("is_primary", "uploaded_at")
    search_fields = ("listing__name", "caption", "alt_text")
    list_editable = ("is_primary",)
    readonly_fields = ("image_preview_large", "uploaded_at")
    
    fieldsets = (
        ("Photo", {
            "fields": ("listing", "image", "image_preview_large")
        }),
        ("Details", {
            "fields": ("caption", "alt_text", "is_primary")
        }),
        ("Metadata", {
            "fields": ("uploaded_at",),
            "classes": ("collapse",)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 60px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.image.url)
        return 'No image uploaded'
    image_preview_large.short_description = 'Image Preview'
