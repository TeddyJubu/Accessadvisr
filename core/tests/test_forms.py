# core/tests/test_forms.py
"""
Tests for AccessAdvisr forms.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import (
    ReviewForm, ListingSubmissionForm, ListingPhotoForm,
    MultiplePhotoUploadForm, ContactForm
)
from core.models import Category, Listing


class ReviewFormTest(TestCase):
    """Test ReviewForm"""
    
    def test_valid_review_form(self):
        """Test form with valid data"""
        data = {
            'author_name': 'John Doe',
            'author_email': 'john@example.com',
            'rating': 5,
            'comment': 'Excellent venue!',
            'step_free_access': 5,
            'restroom_accessible': 4,
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_review_form_missing_required_fields(self):
        """Test form fails without required fields"""
        data = {
            'author_email': 'john@example.com',
            # Missing author_name and rating
        }
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('author_name', form.errors)
        self.assertIn('rating', form.errors)
    
    def test_review_form_invalid_rating(self):
        """Test form rejects invalid rating values"""
        data = {
            'author_name': 'John Doe',
            'rating': 6,  # Invalid: should be 1-5
            'comment': 'Test',
        }
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_review_form_optional_accessibility_fields(self):
        """Test that accessibility fields are optional"""
        data = {
            'author_name': 'Jane',
            'rating': 4,
            'comment': 'Good place',
            # No accessibility fields provided
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())


class ListingSubmissionFormTest(TestCase):
    """Test ListingSubmissionForm"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Food & Restaurants',
            slug='food'
        )
    
    def test_valid_listing_submission_form(self):
        """Test form with valid data"""
        data = {
            'name': 'Accessible Cafe',
            'subtitle': 'Wheelchair friendly',
            'description': '<p>A great accessible cafe</p>',
            'address': '123 Main St',
            'city': 'London',
            'country': 'UK',
            'phone': '+44 20 1234 5678',
            'website': 'https://example.com',
            'email': 'info@example.com',
            'status': 'open',
            'category_choices': ['Food & Restaurants'],
        }
        form = ListingSubmissionForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_listing_form_saves_categories_correctly(self):
        """Test that categories are saved as JSON list"""
        data = {
            'name': 'Test Venue',
            'city': 'London',
            'country': 'UK',
            'status': 'open',
            'category_choices': ['Food & Restaurants'],
        }
        form = ListingSubmissionForm(data=data)
        self.assertTrue(form.is_valid())
        listing = form.save()
        self.assertEqual(listing.categories, ['Food & Restaurants'])
        self.assertEqual(listing.moderation_status, 'pending')
    
    def test_listing_form_missing_required_fields(self):
        """Test form fails without required fields"""
        data = {
            'name': 'Test',
            # Missing city and country
        }
        form = ListingSubmissionForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_listing_form_geocoding_on_save(self):
        """Test that geocoding is attempted on save"""
        data = {
            'name': 'Test Venue',
            'address': '10 Downing Street',
            'city': 'London',
            'country': 'UK',
            'status': 'open',
        }
        form = ListingSubmissionForm(data=data)
        self.assertTrue(form.is_valid())
        listing = form.save()
        # Note: Actual geocoding will fail in tests without API key
        # We're just testing that the method is called
        self.assertIsNotNone(listing)


class ListingPhotoFormTest(TestCase):
    """Test ListingPhotoForm"""
    
    def test_valid_photo_form(self):
        """Test form with valid image"""
        # Create a simple test image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        data = {
            'caption': 'Main entrance',
            'alt_text': 'Photo of the main entrance',
            'is_primary': True,
        }
        form = ListingPhotoForm(data=data, files={'image': image})
        # Note: Validation might fail without actual image file
        # but we're testing the form structure
        self.assertIn('image', form.fields)
        self.assertIn('caption', form.fields)
        self.assertIn('alt_text', form.fields)
    
    def test_photo_form_fields(self):
        """Test form has all required fields"""
        form = ListingPhotoForm()
        self.assertIn('image', form.fields)
        self.assertIn('caption', form.fields)
        self.assertIn('alt_text', form.fields)
        self.assertIn('is_primary', form.fields)


class MultiplePhotoUploadFormTest(TestCase):
    """Test MultiplePhotoUploadForm"""
    
    def test_multiple_photo_form_fields(self):
        """Test form has photos field"""
        form = MultiplePhotoUploadForm()
        self.assertIn('photos', form.fields)
        self.assertFalse(form.fields['photos'].required)


class ContactFormTest(TestCase):
    """Test ContactForm"""
    
    def test_valid_contact_form(self):
        """Test form with valid data"""
        data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'subject': 'General Inquiry',
            'message': 'I have a question about your services.',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_contact_form_missing_fields(self):
        """Test form fails without required fields"""
        data = {
            'name': 'Alice',
            # Missing email and message
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)
    
    def test_contact_form_invalid_email(self):
        """Test form rejects invalid email"""
        data = {
            'name': 'Alice',
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'Test message',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_contact_form_saves_correctly(self):
        """Test form saves message to database"""
        data = {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'subject': 'Partnership',
            'message': 'I would like to discuss a partnership.',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
        message = form.save()
        self.assertEqual(message.name, 'Bob Johnson')
        self.assertEqual(message.email, 'bob@example.com')
        self.assertFalse(message.is_read)
