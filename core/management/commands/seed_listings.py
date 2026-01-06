# core/management/commands/seed_listings.py
from django.core.management.base import BaseCommand
from core.models import Listing

class Command(BaseCommand):
    help = "Seed sample listings for testing"

    def handle(self, *args, **kwargs):
        sample_listings = [
            {
                "name": "Exbury Gardens & Steam Railway",
                "subtitle": "Villa, food for you",
                "categories": ["Food & Restaurants", "Entertainment"],
                "city": "New York",
                "country": "USA",
                "address": "Central Park West, New York, NY",
                "phone": "+88-123-456-789",
                "price_min": 60,
                "price_max": 85,
                "rating": 4.0,
                "status": "open",
                "tags": ["accessible", "wheelchair-friendly"],
                "featured": True,
                "reviews_count": 24,
            },
            {
                "name": "Hotel Sercotel La Boroña",
                "subtitle": "Outdoor, luxury for you",
                "categories": ["Accommodation", "Education"],
                "city": "San Francisco",
                "country": "USA",
                "address": "Fisherman's Wharf, San Francisco, CA",
                "phone": "+89-456-888-666",
                "price_min": 100,
                "price_max": 120,
                "rating": 4.5,
                "status": "open",
                "tags": ["luxury", "accessible"],
                "featured": True,
                "reviews_count": 42,
            },
            {
                "name": "Swansea.com Stadium",
                "subtitle": "Active for you, my friend",
                "categories": ["Sport"],
                "city": "Los Angeles",
                "country": "USA",
                "address": "Downtown Los Angeles, CA",
                "phone": "+89-123-456-789",
                "price_min": 20,
                "price_max": 50,
                "rating": 4.1,
                "status": "open",
                "tags": ["sport", "accessible"],
                "featured": False,
                "reviews_count": 18,
            },
            {
                "name": "The Metropolitan Museum",
                "subtitle": "World-class art and culture",
                "categories": ["Entertainment", "Education"],
                "city": "New York",
                "country": "USA",
                "address": "1000 5th Ave, New York, NY",
                "phone": "+1-212-535-7710",
                "price_min": 25,
                "price_max": 30,
                "rating": 4.8,
                "status": "open",
                "tags": ["museum", "wheelchair-accessible", "audio-guides"],
                "featured": True,
                "reviews_count": 156,
            },
            {
                "name": "Accessible Coffee House",
                "subtitle": "Specialty coffee with accessibility first",
                "categories": ["Food & Drink"],
                "city": "Seattle",
                "country": "USA",
                "address": "Pike Place Market, Seattle, WA",
                "phone": "+1-206-555-0123",
                "price_min": 5,
                "price_max": 15,
                "rating": 4.6,
                "status": "open",
                "tags": ["coffee", "braille-menu", "wide-aisles"],
                "featured": False,
                "reviews_count": 89,
            },
        ]

        created_count = 0
        for data in sample_listings:
            listing, created = Listing.objects.get_or_create(
                name=data["name"],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {listing.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"○ Already exists: {listing.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n✓ Seeding complete. Created {created_count} new listings."))
        self.stdout.write(self.style.SUCCESS(f"Run 'python manage.py geocode_listings' to add coordinates."))
