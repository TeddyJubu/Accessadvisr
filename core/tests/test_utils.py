# core/tests/test_utils.py
"""
Tests for utility functions.
"""
from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
from core.utils import geocode_address, geocode_listing
from core.models import Listing


class GeocodeAddressTest(TestCase):
    """Test geocode_address function"""
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.requests.get')
    def test_geocode_address_success(self, mock_get):
        """Test successful geocoding"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'OK',
            'results': [{
                'geometry': {
                    'location': {
                        'lat': 51.5074,
                        'lng': -0.1278
                    }
                }
            }]
        }
        mock_get.return_value = mock_response
        
        result = geocode_address('10 Downing Street, London, UK')
        self.assertIsNotNone(result)
        self.assertEqual(result, (51.5074, -0.1278))
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.requests.get')
    def test_geocode_address_failure(self, mock_get):
        """Test failed geocoding"""
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ZERO_RESULTS',
            'results': []
        }
        mock_get.return_value = mock_response
        
        result = geocode_address('Invalid Address XYZ123')
        self.assertIsNone(result)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='')
    def test_geocode_address_no_api_key(self):
        """Test geocoding without API key"""
        result = geocode_address('Any Address')
        self.assertIsNone(result)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    def test_geocode_address_empty_input(self):
        """Test geocoding with empty address"""
        result = geocode_address('')
        self.assertIsNone(result)
        
        result = geocode_address('   ')
        self.assertIsNone(result)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.requests.get')
    def test_geocode_address_timeout(self, mock_get):
        """Test geocoding timeout handling"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = geocode_address('Some Address')
        self.assertIsNone(result)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.requests.get')
    def test_geocode_address_network_error(self, mock_get):
        """Test network error handling"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException('Network error')
        
        result = geocode_address('Some Address')
        self.assertIsNone(result)


class GeocodeListingTest(TestCase):
    """Test geocode_listing function"""
    
    def setUp(self):
        self.listing = Listing.objects.create(
            name='Test Venue',
            address='123 Main St',
            city='London',
            country='UK'
        )
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.geocode_address')
    def test_geocode_listing_success(self, mock_geocode):
        """Test successful listing geocoding"""
        mock_geocode.return_value = (51.5074, -0.1278)
        
        result = geocode_listing(self.listing)
        self.assertTrue(result)
        
        # Refresh from database
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.lat, 51.5074)
        self.assertEqual(self.listing.lng, -0.1278)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.geocode_address')
    def test_geocode_listing_failure(self, mock_geocode):
        """Test failed listing geocoding"""
        mock_geocode.return_value = None
        
        result = geocode_listing(self.listing)
        self.assertFalse(result)
        
        # Coordinates should remain None
        self.listing.refresh_from_db()
        self.assertIsNone(self.listing.lat)
        self.assertIsNone(self.listing.lng)
    
    def test_geocode_listing_no_address_info(self):
        """Test geocoding listing without address information"""
        listing = Listing.objects.create(name='No Address Venue')
        
        result = geocode_listing(listing)
        self.assertFalse(result)
    
    @override_settings(GOOGLE_MAPS_SERVER_KEY='test_api_key')
    @patch('core.utils.geocode_address')
    def test_geocode_listing_city_country_only(self, mock_geocode):
        """Test geocoding with only city and country"""
        listing = Listing.objects.create(
            name='City Only Venue',
            city='Paris',
            country='France'
        )
        mock_geocode.return_value = (48.8566, 2.3522)
        
        result = geocode_listing(listing)
        self.assertTrue(result)
        
        # Check the address string passed to geocode_address
        mock_geocode.assert_called_once_with('Paris, France')
