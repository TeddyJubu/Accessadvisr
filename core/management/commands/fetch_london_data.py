import os
import requests
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Listing

class Command(BaseCommand):
    help = "Fetch 50 real accessible venues in London using Google Places API"

    def handle(self, *args, **kwargs):
        api_key = os.getenv("GOOGLE_MAPS_SERVER_KEY") or settings.GOOGLE_MAPS_SERVER_KEY
        if not api_key:
            self.stdout.write(self.style.ERROR("GOOGLE_MAPS_SERVER_KEY not found in environment or settings."))
            return

        queries = [
            "wheelchair accessible museums in London",
            "wheelchair accessible restaurants in London",
            "wheelchair accessible tourist attractions in London",
            "wheelchair accessible hotels in London",
            "wheelchair accessible cafes in London"
        ]

        venues_found = []
        
        for query in queries:
            if len(venues_found) >= 50:
                break
                
            self.stdout.write(f"Searching for: {query}...")
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query.replace(' ', '+')}&key={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data.get("status") == "OK":
                for result in data.get("results", []):
                    if result.get("place_id") not in [v["place_id"] for v in venues_found]:
                        venues_found.append({
                            "place_id": result.get("place_id"),
                            "name": result.get("name"),
                            "address": result.get("formatted_address"),
                            "lat": result.get("geometry", {}).get("location", {}).get("lat"),
                            "lng": result.get("geometry", {}).get("location", {}).get("lng"),
                            "rating": result.get("rating", 0),
                            "reviews_count": result.get("user_ratings_total", 0),
                            "types": result.get("types", []),
                            "photo_reference": result.get("photos", [{}])[0].get("photo_reference") if result.get("photos") else None
                        })
                        if len(venues_found) >= 50:
                            break
            else:
                self.stdout.write(self.style.WARNING(f"Search failed for {query}: {data.get('status')}"))
            
            # Rate limiting / polite delay
            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(f"Found {len(venues_found)} venues. Now fetching details..."))

        created_count = 0
        for venue in venues_found:
            # Fetch place details for more info
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={venue['place_id']}&fields=website,formatted_phone_number,opening_hours,wheelchair_accessible_entrance,editorial_summary&key={api_key}"
            details_resp = requests.get(details_url).json()
            details = details_resp.get("result", {})

            # Map categories
            cats = []
            if any(t in venue["types"] for t in ["restaurant", "cafe", "bar", "food"]):
                cats.append("Food & Drink")
            if any(t in venue["types"] for t in ["museum", "art_gallery", "tourist_attraction", "stadium"]):
                cats.append("Entertainment")
            if "lodging" in venue["types"]:
                cats.append("Accommodation")
            if any(t in venue["types"] for t in ["library", "university"]):
                cats.append("Education")
            if not cats:
                cats.append("Entertainment") # Default

            # Accessibility features
            features = []
            if details.get("wheelchair_accessible_entrance"):
                features.append("wheelchair")
            
            # Build photo URL if possible
            photo_url = ""
            if venue["photo_reference"]:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={venue['photo_reference']}&key={api_key}"

            # Create Listing
            listing, created = Listing.objects.update_or_create(
                name=venue["name"],
                defaults={
                    "subtitle": details.get("editorial_summary", {}).get("overview", "")[:200],
                    "description": details.get("editorial_summary", {}).get("overview", ""),
                    "categories": cats,
                    "city": "London",
                    "country": "UK",
                    "address": venue["address"],
                    "lat": venue["lat"],
                    "lng": venue["lng"],
                    "phone": details.get("formatted_phone_number", ""),
                    "website": details.get("website", ""),
                    "status": "open",
                    "rating": venue["rating"],
                    "reviews_count": venue["reviews_count"],
                    "photos": [photo_url] if photo_url else [],
                    "accessibility_features": features,
                    "moderation_status": "approved"
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"✓ Added: {listing.name}")
            else:
                self.stdout.write(f"○ Updated: {listing.name}")
            
            # Delay to avoid hitting rate limits
            time.sleep(0.05)

        self.stdout.write(self.style.SUCCESS(f"\nDone! Added/Updated {created_count} listings from London."))
