# core/admin.py
from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'rating', 'status', 'lat', 'lng')
    list_filter = ('status', 'featured', 'country')
    search_fields = ('name', 'city', 'country', 'address')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'subtitle', 'status', 'featured')
        }),
        ('Location', {
            'fields': ('address', 'city', 'country', 'lat', 'lng')
        }),
        ('Details', {
            'fields': ('categories', 'tags', 'phone', 'price_min', 'price_max')
        }),
        ('Ratings', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
