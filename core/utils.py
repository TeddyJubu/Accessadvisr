# core/utils.py
"""
Utility functions for the AccessAdvisr application.
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def geocode_address(address: str) -> tuple[float, float] | None:
    """
    Geocode an address string using Google's Geocoding API.
    
    Args:
        address: The address string to geocode (e.g., "123 Main St, New York, NY")
    
    Returns:
        A tuple of (latitude, longitude) if successful, None if failed.
    
    Example:
        >>> coords = geocode_address("Central Park, New York")
        >>> if coords:
        ...     lat, lng = coords
        ...     print(f"Location: {lat}, {lng}")
    """
    key = settings.GOOGLE_MAPS_SERVER_KEY
    
    if not key:
        logger.warning("GOOGLE_MAPS_SERVER_KEY not configured - geocoding skipped")
        return None
    
    if not address or not address.strip():
        logger.warning("Empty address provided for geocoding")
        return None
    
    try:
        response = requests.get(
            GEOCODE_URL,
            params={"address": address, "key": key},
            timeout=10
        )
        data = response.json()
        
        if data.get("status") == "OK" and data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            logger.info(f"Successfully geocoded '{address}' -> ({lat}, {lng})")
            return (lat, lng)
        else:
            status = data.get("status", "UNKNOWN")
            error_msg = data.get("error_message", "No error message")
            logger.warning(f"Geocoding failed for '{address}': {status} - {error_msg}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding timeout for '{address}'")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding request error for '{address}': {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Geocoding response parsing error for '{address}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected geocoding error for '{address}': {str(e)}")
        return None


def geocode_listing(listing) -> bool:
    """
    Geocode a Listing object using its address or city/country.
    Updates the listing's lat/lng fields if successful.
    
    Args:
        listing: A Listing model instance
        
    Returns:
        True if geocoding was successful and the listing was updated,
        False otherwise.
    """
    # Build the best address string we have
    address_parts = []
    
    if listing.address:
        address_parts.append(listing.address)
    if listing.city:
        address_parts.append(listing.city)
    if listing.country:
        address_parts.append(listing.country)
    
    if not address_parts:
        logger.warning(f"Listing '{listing.name}' has no address information for geocoding")
        return False
    
    address = ", ".join(address_parts)
    coords = geocode_address(address)
    
    if coords:
        listing.lat, listing.lng = coords
        listing.save(update_fields=["lat", "lng"])
        return True
    
    return False
