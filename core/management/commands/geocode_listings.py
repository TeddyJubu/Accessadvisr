# core/management/commands/geocode_listings.py
import requests
from django.core.management.base import BaseCommand
from core.models import Listing
from django.conf import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

class Command(BaseCommand):
    help = "Geocode listings with missing lat/lng"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Preview which listings would be geocoded without making API calls"
        )
        parser.add_argument(
            "--limit", type=int, default=100,
            help="Maximum number of listings to process (default: 100)"
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        key = settings.GOOGLE_MAPS_SERVER_KEY
        
        if not key and not dry_run:
            self.stdout.write(self.style.ERROR("GOOGLE_MAPS_SERVER_KEY not set. Use --dry-run to preview."))
            return
        
        listings_to_geocode = Listing.objects.filter(lat__isnull=True) | Listing.objects.filter(lng__isnull=True)
        listings_to_geocode = listings_to_geocode[:limit]
        total = listings_to_geocode.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No listings need geocoding."))
            return
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f"[DRY RUN] Would geocode {total} listings:"))
            for l in listings_to_geocode:
                query = l.address or l.location_text()
                self.stdout.write(f"  • {l.name}: {query}")
            return
        
        self.stdout.write(f"Geocoding {total} listings...")
        
        for l in listings_to_geocode:
            query = l.address or l.location_text()
            try:
                resp = requests.get(
                    GEOCODE_URL, 
                    params={"address": query, "key": key}, 
                    timeout=10
                ).json()
                
                if resp.get("status") == "OK":
                    loc = resp["results"][0]["geometry"]["location"]
                    l.lat, l.lng = loc["lat"], loc["lng"]
                    l.save(update_fields=["lat", "lng"])
                    self.stdout.write(self.style.SUCCESS(f"✓ Geocoded: {l.name} -> {l.lat},{l.lng}"))
                else:
                    self.stdout.write(self.style.WARNING(f"✗ Failed: {l.name} ({resp.get('status')})"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error geocoding {l.name}: {str(e)}"))
