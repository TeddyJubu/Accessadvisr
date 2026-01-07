# core/tests/test_views.py
"""
Comprehensive tests for AccessAdvisr views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import (
    Listing, Review, Category, BlogPost, BlogCategory,
    ContactMessage, Partner, SponsorshipPackage, DonationGoal
)


class HomeViewTest(TestCase):
    """Test home page view"""
    
    def setUp(self):
        self.client = Client()
        # Create some test listings
        self.listing1 = Listing.objects.create(
            name="Featured Cafe",
            city="London",
            country="UK",
            featured=True,
            moderation_status="approved"
        )
        self.listing2 = Listing.objects.create(
            name="Regular Restaurant",
            city="London",
            country="UK",
            moderation_status="approved"
        )
    
    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
    
    def test_home_page_shows_featured_listings(self):
        """Test featured listings are displayed"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Featured Cafe")


class ListingsListViewTest(TestCase):
    """Test listings list view"""
    
    def setUp(self):
        self.client = Client()
        # Create test listings
        for i in range(15):
            Listing.objects.create(
                name=f"Venue {i}",
                city="London",
                country="UK",
                moderation_status="approved"
            )
    
    def test_listings_page_loads(self):
        """Test listings page loads successfully"""
        response = self.client.get(reverse('listings_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/listings_list.html')
    
    def test_listings_pagination(self):
        """Test pagination works correctly"""
        response = self.client.get(reverse('listings_list'))
        self.assertTrue(response.context['is_paginated'])
        # Default pagination is 12 per page
        self.assertEqual(len(response.context['listings']), 12)
    
    def test_listings_search(self):
        """Test search functionality"""
        Listing.objects.create(
            name="Unique Accessible Cafe",
            city="London",
            country="UK",
            moderation_status="approved"
        )
        response = self.client.get(reverse('listings_list'), {'search': 'Unique'})
        self.assertContains(response, "Unique Accessible Cafe")
    
    def test_listings_city_filter(self):
        """Test city filtering"""
        Listing.objects.create(
            name="Paris Restaurant",
            city="Paris",
            country="France",
            moderation_status="approved"
        )
        response = self.client.get(reverse('listings_list'), {'city': 'Paris'})
        self.assertContains(response, "Paris Restaurant")
    
    def test_pending_listings_not_shown(self):
        """Test that pending listings are not displayed"""
        Listing.objects.create(
            name="Pending Venue",
            city="London",
            country="UK",
            moderation_status="pending"
        )
        response = self.client.get(reverse('listings_list'))
        self.assertNotContains(response, "Pending Venue")


class ListingDetailViewTest(TestCase):
    """Test listing detail view"""
    
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(
            name="Test Restaurant",
            city="London",
            country="UK",
            description="<p>A test restaurant</p>",
            moderation_status="approved"
        )
        # Add some reviews
        Review.objects.create(
            listing=self.listing,
            author_name="John",
            rating=5,
            comment="Excellent!",
            moderation_status="approved"
        )
    
    def test_listing_detail_loads(self):
        """Test listing detail page loads"""
        response = self.client.get(reverse('listing_detail', args=[self.listing.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/listing_detail.html')
        self.assertContains(response, "Test Restaurant")
    
    def test_listing_detail_shows_reviews(self):
        """Test approved reviews are displayed"""
        response = self.client.get(reverse('listing_detail', args=[self.listing.pk]))
        self.assertContains(response, "John")
        self.assertContains(response, "Excellent!")
    
    def test_listing_detail_404_for_nonexistent(self):
        """Test 404 for non-existent listing"""
        response = self.client.get(reverse('listing_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class SubmitReviewViewTest(TestCase):
    """Test review submission view"""
    
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(
            name="Test Venue",
            city="London",
            country="UK",
            moderation_status="approved"
        )
    
    def test_submit_review_post(self):
        """Test submitting a review"""
        data = {
            'author_name': 'Jane Doe',
            'author_email': 'jane@example.com',
            'rating': 4,
            'comment': 'Great place!',
            'step_free_access': 5,
            'restroom_accessible': 4,
        }
        response = self.client.post(
            reverse('submit_review', args=[self.listing.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check review was created
        review = Review.objects.filter(listing=self.listing).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.author_name, 'Jane Doe')
        self.assertEqual(review.moderation_status, 'pending')
    
    def test_submit_review_invalid_data_form(self):
        """Test form validation with invalid data"""
        from core.forms import ReviewForm
        data = {
            'author_name': '',  # Required field
            'rating': 3,
        }
        form = ReviewForm(data=data)
        # Should have validation errors
        self.assertFalse(form.is_valid())
        self.assertIn('author_name', form.errors)


class SubmitListingViewTest(TestCase):
    """Test listing submission view"""
    
    def setUp(self):
        self.client = Client()
        Category.objects.create(name="Food", slug="food")
    
    def test_submit_listing_get(self):
        """Test submit listing form page loads"""
        response = self.client.get(reverse('submit_listing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/submit_listing.html')
    
    def test_submit_listing_post(self):
        """Test submitting a new listing"""
        data = {
            'name': 'New Accessible Cafe',
            'subtitle': 'Wheelchair Friendly',
            'description': '<p>A new accessible venue</p>',
            'address': '456 Test St',
            'city': 'London',
            'country': 'UK',
            'phone': '+44 20 1234 5678',
            'website': 'https://example.com',
            'email': 'info@example.com',
            'status': 'open',
            'category_choices': ['Food'],
        }
        response = self.client.post(reverse('submit_listing'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check listing was created with pending status
        listing = Listing.objects.filter(name='New Accessible Cafe').first()
        self.assertIsNotNone(listing)
        self.assertEqual(listing.moderation_status, 'pending')


class ContactViewTest(TestCase):
    """Test contact form view"""
    
    def setUp(self):
        self.client = Client()
    
    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
    
    def test_contact_form_submission(self):
        """Test submitting contact form"""
        data = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'subject': 'Question',
            'message': 'I have a question about your service.',
        }
        response = self.client.post(reverse('contact'), data)
        
        # Check message was saved
        message = ContactMessage.objects.filter(email='alice@example.com').first()
        self.assertIsNotNone(message)
        self.assertEqual(message.name, 'Alice')
        self.assertFalse(message.is_read)


class BlogViewsTest(TestCase):
    """Test blog views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
        self.category = BlogCategory.objects.create(
            name='Travel',
            slug='travel'
        )
        self.post = BlogPost.objects.create(
            title='Accessible London',
            slug='accessible-london',
            category=self.category,
            author=self.user,
            content='<p>Guide to accessible London</p>',
            excerpt='A guide to London',
            is_published=True
        )
    
    def test_blog_list_loads(self):
        """Test blog list page loads"""
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog_list.html')
        self.assertContains(response, 'Accessible London')
    
    def test_blog_detail_loads(self):
        """Test blog detail page loads"""
        response = self.client.get(reverse('blog_detail', args=['accessible-london']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog_detail.html')
        self.assertContains(response, 'Accessible London')
    
    def test_unpublished_posts_not_shown(self):
        """Test unpublished posts are not displayed"""
        unpublished = BlogPost.objects.create(
            title='Draft Post',
            slug='draft',
            category=self.category,
            content='<p>Draft content</p>',
            is_published=False
        )
        response = self.client.get(reverse('blog_list'))
        self.assertNotContains(response, 'Draft Post')


class ListingsAPIViewTest(TestCase):
    """Test listings API endpoint"""
    
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(
            name="API Test Venue",
            city="London",
            country="UK",
            lat=51.5074,
            lng=-0.1278,
            moderation_status="approved"
        )
    
    def test_listings_api_returns_json(self):
        """Test API returns JSON response"""
        response = self.client.get(reverse('listings_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_listings_api_includes_coordinates(self):
        """Test API includes lat/lng for map display"""
        response = self.client.get(reverse('listings_api'))
        data = response.json()
        self.assertGreater(len(data), 0)
        listing_data = data[0]
        self.assertEqual(listing_data['name'], 'API Test Venue')
        self.assertEqual(listing_data['lat'], 51.5074)
        self.assertEqual(listing_data['lng'], -0.1278)


class StaticPagesTest(TestCase):
    """Test static pages"""
    
    def setUp(self):
        self.client = Client()
    
    def test_about_page_loads(self):
        """Test about page loads"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
    
    def test_partners_page_loads(self):
        """Test partners page loads"""
        response = self.client.get(reverse('partners'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/partners.html')
    
    def test_packages_page_loads(self):
        """Test sponsorship packages page loads"""
        response = self.client.get(reverse('packages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/packages.html')
    
    def test_donate_page_loads(self):
        """Test donate page loads"""
        response = self.client.get(reverse('donate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/donate.html')
