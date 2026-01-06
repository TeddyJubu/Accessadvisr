# core/management/commands/geocode_listings.py
import requests
from django.core.management.base import BaseCommand
from core.models import Listing
from django.conf import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

class Command(BaseCommand):
    help = "Geocode listings with missing lat/lng"

    def handle(self, *args, **kwargs):
        key = settings.GOOGLE_MAPS_SERVER_KEY
        
        if not key:
            self.stdout.write(self.style.ERROR("GOOGLE_MAPS_SERVER_KEY not set. Please set it in your environment."))
            return
        
        listings_to_geocode = Listing.objects.filter(lat__isnull=True, lng__isnull=True)
        total = listings_to_geocode.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No listings need geocoding."))
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
