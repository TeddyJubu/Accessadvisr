# core/context_processors.py
from django.conf import settings

def google_maps_key(request):
    """Expose Google Maps browser key to all templates"""
    return {
        'GOOGLE_MAPS_BROWSER_KEY': settings.GOOGLE_MAPS_BROWSER_KEY,
    }
