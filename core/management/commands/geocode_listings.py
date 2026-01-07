# core/management/commands/geocode_listings.py
"""
Management command to geocode listings that are missing coordinates.
"""
from django.core.management.base import BaseCommand
from core.models import Listing
from core.utils import geocode_listing
from django.conf import settings


class Command(BaseCommand):
    help = "Geocode listings with missing lat/lng coordinates"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Preview which listings would be geocoded without making API calls"
        )
        parser.add_argument(
            "--limit", type=int, default=100,
            help="Maximum number of listings to process (default: 100)"
        )
        parser.add_argument(
            "--force", action="store_true",
            help="Re-geocode all listings, even those with existing coordinates"
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        force = options["force"]
        key = settings.GOOGLE_MAPS_SERVER_KEY
        
        # Check API key
        if not key and not dry_run:
            self.stdout.write(self.style.ERROR(
                "❌ GOOGLE_MAPS_SERVER_KEY not set.\n"
                "   Add it to your .env file or use --dry-run to preview."
            ))
            return
        
        # Get listings to geocode
        if force:
            listings_to_geocode = Listing.objects.all()[:limit]
            self.stdout.write(self.style.WARNING("Force mode: re-geocoding all listings"))
        else:
            listings_to_geocode = (
                Listing.objects.filter(lat__isnull=True) | 
                Listing.objects.filter(lng__isnull=True)
            )[:limit]
        
        total = listings_to_geocode.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS("✓ All listings already have coordinates."))
            return
        
        # Dry run - just show what would be geocoded
        if dry_run:
            self.stdout.write(self.style.WARNING(f"\n[DRY RUN] Would geocode {total} listing(s):\n"))
            for listing in listings_to_geocode:
                address = listing.address or listing.location_text()
                coords = f"({listing.lat}, {listing.lng})" if listing.lat else "No coordinates"
                self.stdout.write(f"  • {listing.name}")
                self.stdout.write(f"    Address: {address}")
                self.stdout.write(f"    Current: {coords}\n")
            return
        
        # Actually geocode
        self.stdout.write(f"\n🌍 Geocoding {total} listing(s)...\n")
        
        success_count = 0
        fail_count = 0
        
        for listing in listings_to_geocode:
            address = listing.address or listing.location_text()
            self.stdout.write(f"  Processing: {listing.name}")
            
            if geocode_listing(listing):
                success_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"    ✓ Geocoded → ({listing.lat:.6f}, {listing.lng:.6f})"
                ))
            else:
                fail_count += 1
                self.stdout.write(self.style.WARNING(
                    f"    ✗ Failed to geocode: {address}"
                ))
        
        # Summary
        self.stdout.write("")
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"✓ Successfully geocoded: {success_count}"))
        if fail_count > 0:
            self.stdout.write(self.style.WARNING(f"✗ Failed to geocode: {fail_count}"))
        
        self.stdout.write(self.style.SUCCESS("\nDone!"))
