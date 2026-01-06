Here’s a practical, iterative plan to implement the core map feature with Google Maps in your Django + HTML setup. It covers data modeling, server endpoints, client initialization, filters, geocoding, and accessibility, with code snippets you can drop in.

Architecture and data flow

- Server (Django):

 ▫ Persist venue listings with latitude/longitude.

 ▫ Provide JSON endpoints for listings and server-side geocoding.

- Client (HTML/JS):

 ▫ Initialize Google Map.

 ▫ Fetch listings as GeoJSON/JSON.

 ▫ Render markers with clustering.

 ▫ Wire search filters to client-side requests and map updates.

1) Keys and setup

- Create two API keys:

 ▫ Browser key: restricted to your domain and APIs: Maps JavaScript API, Places API.

 ▫ Server key: restricted by IP; APIs: Geocoding API (and optionally Distance Matrix).

- In Django settings:

 ▫ Add environment variables and expose browser key to templates.

# settings.py

import os

GOOGLE_MAPS_BROWSER_KEY = os.getenv("GOOGLE_MAPS_BROWSER_KEY", "")

GOOGLE_MAPS_SERVER_KEY = os.getenv("GOOGLE_MAPS_SERVER_KEY", "")

- In base template, include Maps JS with your browser key:

<script async defer src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_BROWSER_KEY }}&libraries=places"></script>

2) Data model

Persist lat/lng so the map doesn’t geocode every render.# core/models.py

from django.db import models

class Listing(models.Model):

    name = models.CharField(max_length=200)

    subtitle = models.CharField(max_length=200, blank=True)

    categories = models.JSONField(default=list)  # ["Food & Restaurants", "Sport"]

    city = models.CharField(max_length=120)

    country = models.CharField(max_length=120)

    address = models.CharField(max_length=255, blank=True)  # optional full address

    phone = models.CharField(max_length=40, blank=True)

    price_min = models.IntegerField(null=True, blank=True)

    price_max = models.IntegerField(null=True, blank=True)

    rating = models.FloatField(default=0)

    status = models.CharField(max_length=20, default="open")  # open|closed

    tags = models.JSONField(default=list)

    featured = models.BooleanField(default=False)

    reviews_count = models.IntegerField(default=0)

    lat = models.FloatField(null=True, blank=True)

    lng = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def location_text(self):

        return f"{self.city}, {self.country}"

3) Seed + geocode lat/lng (server-side)

Perform geocoding once, store results.# core/management/commands/geocode_listings.py

import os, requests

from django.core.management.base import BaseCommand

from core.models import Listing

from django.conf import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

class Command(BaseCommand):

    help = "Geocode listings with missing lat/lng"

    def handle(self, *args, **kwargs):

        key = settings.GOOGLE_MAPS_SERVER_KEY

        for l in Listing.objects.filter(lat__isnull=True, lng__isnull=True):

            query = l.address or l.location_text()

            resp = requests.get(GEOCODE_URL, params={"address": query, "key": key}, timeout=10).json()

            if resp.get("status") == "OK":

                loc = resp["results"][0]["geometry"]["location"]

                l.lat, l.lng = loc["lat"], loc["lng"]

                l.save(update_fields=["lat", "lng"])

                self.stdout.write(self.style.SUCCESS(f"Geocoded: {l.name} -> {l.lat},{l.lng}"))

            else:

                self.stdout.write(self.style.WARNING(f"Failed: {l.name} ({resp.get('status')})"))

4) JSON API endpoints

Return listings filtered by query, category, and location.# core/views.py

from django.http import JsonResponse

from django.db.models import Q

from .models import Listing

def listings_api(request):

    q = request.GET.get("q", "").strip()

    category = request.GET.get("category", "").strip()

    location = request.GET.get("location", "").strip()

    qs = Listing.objects.all()

    if q:

        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q))

    if category:

        qs = qs.filter(categories__icontains=category)  # simple contains on JSON

    if location:

        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))

    data = [{

        "id": l.id,

        "name": l.name,

        "subtitle": l.subtitle,

        "categories": l.categories,

        "city": l.city, "country": l.country,

        "phone": l.phone,

        "priceMin": l.price_min, "priceMax": l.price_max,

        "rating": l.rating, "status": l.status,

        "reviewsCount": l.reviews_count,

        "lat": l.lat, "lng": l.lng,

    } for l in qs if l.lat is not None and l.lng is not None]

    return JsonResponse({"listings": data})

Wire URL:# core/urls.py

from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('admin-page/', views.admin_page, name='admin_page'),

    path('api/listings/', views.listings_api, name='listings_api'),

]

5) Client-side: map initialization and markers

Create a partial for scripts to keep home clean; this ties into your search bar inputs.<!-- templates/core/partials/scripts.html -->

<script>

(function(){

  let map, markers = [], markerCluster, infoWindow;

  const apiUrl = "{% url 'listings_api' %}";

  function initMap(){

    map = new google.maps.Map(document.getElementById('map-root'), {

      center: { lat: 40.7128, lng: -74.0060 }, // NYC default

      zoom: 11,

      mapTypeControl: false,

      streetViewControl: false

    });

    infoWindow = new google.maps.InfoWindow();

    loadListings();

    // Places Autocomplete for location input (optional)

    const locInput = document.querySelector('[aria-label="Location"]');

    if (locInput) {

      const autocomplete = new google.maps.places.Autocomplete(locInput, {

        types: ['(cities)']

      });

      autocomplete.addListener('place_changed', () => {

        const place = autocomplete.getPlace();

        if (place.geometry && place.geometry.location) {

          map.panTo(place.geometry.location);

          map.setZoom(12);

        }

        submitSearch();

      });

    }

  }

  function clearMarkers(){

    markers.forEach(m => m.setMap(null));

    markers = [];

    if (markerCluster) { markerCluster.clearMarkers(); markerCluster = null; }

  }

  async function loadListings(params={}){

    const url = new URL(apiUrl, window.location.origin);

    Object.entries(params).forEach(([k,v])=>{ if(v) url.searchParams.set(k, v); });

    const res = await fetch(url.toString());

    const json = await res.json();

    renderMarkers(json.listings);

  }

  function renderMarkers(listings){

    clearMarkers();

    listings.forEach(l => {

      const marker = new google.maps.Marker({

        position: { lat: l.lat, lng: l.lng },

        map,

        title: l.name,

        label: l.rating ? { text: String(l.rating), color: 'white', className: 'marker-label' } : undefined,

      });

      marker.addListener('click', () => {

        infoWindow.setContent(`

          <div class="p-2">

            <div class="font-bold">${l.name}</div>

            <div class="text-sm text-slate-600">${l.subtitle || ''}</div>

            <div class="mt-1 text-xs">${l.city}, ${l.country}</div>

            <div class="mt-1 text-xs">$${l.priceMin ?? ''} - $${l.priceMax ?? ''}</div>

            <div class="mt-1 text-xs">${l.status?.toUpperCase()}</div>

            <div class="mt-1 text-xs">${l.categories?.join(', ')}</div>

          </div>

        `);

        infoWindow.open(map, marker);

      });

      markers.push(marker);

    });

    // Optional clustering (use @googlemaps/markerclusterer)

    // If you prefer CDN, include it in base head:

    // <script src="https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js"></script>

    if (window.markerClusterer) {

      markerCluster = new markerClusterer.MarkerClusterer({ map, markers });

    }

    if (listings.length) {

      const bounds = new google.maps.LatLngBounds();

      listings.forEach(l => bounds.extend({lat: l.lat, lng: l.lng}));

      map.fitBounds(bounds, 64);

    }

  }

  function submitSearch(){

    const q = document.querySelector('[aria-label="Keywords"]')?.value || '';

    const category = document.querySelector('[aria-label="Filter by category"]')?.value || '';

    const location = document.querySelector('[aria-label="Location"]')?.value || '';

    loadListings({ q, category, location });

  }

  // Wire search button

  document.addEventListener('DOMContentLoaded', () => {

    const btn = document.querySelector('.shadow-orange-200');

    btn?.addEventListener('click', (e) => { e.preventDefault(); submitSearch(); });

    // Create a map root overlay behind hero pattern

    const hero = document.querySelector('section.relative.w-full.h-\\[600px\\]');

    if (hero) {

      const mapRoot = document.createElement('div');

      mapRoot.id = 'map-root';

      mapRoot.className = 'absolute inset-0';

      hero.appendChild(mapRoot);

    }

    // Initialize after Google script loads

    if (window.google && window.google.maps) initMap();

    else window.addEventListener('load', () => {

      if (window.google && window.google.maps) initMap();

    });

  });

})();

</script>

<style>

/* Optional marker label styling */

.marker-label {

  background-color: #FF431E;

  color: white;

  padding: 2px 4px;

  border-radius: 4px;

  font-weight: 700;

}

</style>

Notes:

- The script injects a real Google Map into your existing hero section by adding a #map-root div.

- It connects the existing search inputs to the API endpoint.

- It uses Places Autocomplete on the location field to pan the map and trigger filtering.

- To enable clustering via CDN, add this in base.html head:

<script src="https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js"></script>

6) Server-side geosearch (optional enhancement)

For location filtering beyond simple text, accept a lat/lng and radius; compute bounding box or haversine.# core/views.py (enhanced)

import math

def listings_api(request):

    # ... previous filters

    center_lat = request.GET.get("lat")

    center_lng = request.GET.get("lng")

    radius_km = float(request.GET.get("radius", "0") or 0)

    qs = Listing.objects.all()

    # filters ...

    if center_lat and center_lng and radius_km > 0:

        lat = float(center_lat); lng = float(center_lng)

        # crude bounding box first

        lat_delta = radius_km / 111.0

        lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)) or 1)

        qs = qs.filter(

            lat__gte=lat - lat_delta, lat__lte=lat + lat_delta,

            lng__gte=lng - lng_delta, lng__lte=lng + lng_delta

        )

    # return JSON as before

Client can pass the map center and radius from current bounds.

7) Accessibility and progressive enhancement

- Keep the list view of cards as a non-map alternative; treat the map as an enhancement.

- Provide alt text for images; for the map canvas, add a descriptive label near it: “Interactive map of accessibility listings.”

- Ensure keyboard focus styles and that infoWindow content is readable with sufficient contrast.

8) Performance and quotas

- Cache listings JSON for 30–60 seconds to reduce DB hits:

# core/views.py

from django.views.decorators.cache import cache_page

@cache_page(30)

def listings_api(request): ...

- Geocode only on create/update; avoid client-side geocoding of many items.

- Restrict keys: HTTP referrer restrictions for browser key; IP restrictions for server key.

9) Iterative steps to ship

1. Migrate model, seed a few records, run geocode command to fill lat/lng.

2. Add Maps script with browser key; add scripts partial above; confirm map renders with markers.

3. Connect search inputs to API; verify filtering updates markers and fits bounds.

4. Add Places Autocomplete; pan map and reload markers.

5. Optional: add clustering and server-side radius filtering using map bounds.

10) Future features

- Directions and travel times: Distance Matrix API from user’s location to venues.

- Save/favorite: store per-user later when auth is added.

- Category coloring: different marker icons per category for quick visual scanning.

This plan keeps your current HTML intact, adds a real interactive map, and evolves cleanly with Django’s server-side capabilities while respecting accessibility and performance.