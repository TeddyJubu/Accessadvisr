# core/views.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models import Listing

def home(request):
    return render(request, "core/home.html")

@require_http_methods(["GET", "POST"])
def admin_page(request):
    if request.method == "POST":
        # TODO: in future, seed DB; for now just redirect with a flash message stub
        return redirect("admin_page")
    return render(request, "core/admin.html")

@cache_page(30)
def listings_api(request):
    """API endpoint for listings with filtering"""
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    location = request.GET.get("location", "").strip()
    
    qs = Listing.objects.all()
    
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(subtitle__icontains=q))
    
    if category and category != "Filter by category":
        qs = qs.filter(categories__icontains=category)  # simple contains on JSON
    
    if location:
        qs = qs.filter(Q(city__icontains=location) | Q(country__icontains=location))
    
    data = [{
        "id": l.id,
        "name": l.name,
        "subtitle": l.subtitle,
        "categories": l.categories,
        "city": l.city, 
        "country": l.country,
        "phone": l.phone,
        "priceMin": l.price_min, 
        "priceMax": l.price_max,
        "rating": l.rating, 
        "status": l.status,
        "reviewsCount": l.reviews_count,
        "lat": l.lat, 
        "lng": l.lng,
    } for l in qs if l.lat is not None and l.lng is not None]
    
    return JsonResponse({"listings": data})
