# core/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import Category, Listing, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


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
        "status", "moderation_status", "has_coordinates"
    )
    list_filter = ("status", "moderation_status", "featured", "country")
    search_fields = ("name", "city", "country", "address")
    readonly_fields = ("rating", "reviews_count", "created_at", "updated_at")
    list_editable = ("moderation_status",)
    inlines = [ReviewInline]
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
