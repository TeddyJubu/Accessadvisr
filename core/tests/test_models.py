# core/tests/test_models.py
"""
Comprehensive tests for AccessAdvisr models.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from core.models import (
    Category, Listing, ListingPhoto, Review,
    TeamMember, Partner, ContactMessage,
    BlogCategory, BlogPost, SponsorshipPackage, DonationGoal
)


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Food & Restaurants",
            slug="food-restaurants",
            icon="utensils",
            color="#FF5733"
        )
    
    def test_category_creation(self):
        """Test basic category creation"""
        self.assertEqual(self.category.name, "Food & Restaurants")
        self.assertEqual(self.category.slug, "food-restaurants")
        self.assertEqual(str(self.category), "Food & Restaurants")
    
    def test_category_unique_constraint(self):
        """Test that category names must be unique"""
        with self.assertRaises(Exception):
            Category.objects.create(
                name="Food & Restaurants",
                slug="food-restaurants-2"
            )
    
    def test_category_ordering(self):
        """Test categories are ordered by name"""
        Category.objects.create(name="Accommodation", slug="accommodation")
        Category.objects.create(name="Zoos", slug="zoos")
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "Accommodation")


class ListingModelTest(TestCase):
    """Test Listing model"""
    
    def setUp(self):
        self.listing = Listing.objects.create(
            name="The Accessible Cafe",
            subtitle="Wheelchair-friendly dining",
            description="<p>A beautiful accessible cafe</p>",
            city="London",
            country="United Kingdom",
            address="123 Main St",
            lat=51.5074,
            lng=-0.1278,
            phone="+44 20 1234 5678",
            website="https://example.com",
            email="cafe@example.com",
            price_min=10,
            price_max=30,
            status="open",
            moderation_status="approved"
        )
    
    def test_listing_creation(self):
        """Test basic listing creation"""
        self.assertEqual(self.listing.name, "The Accessible Cafe")
        self.assertEqual(self.listing.rating, 0)
        self.assertEqual(self.listing.reviews_count, 0)
        self.assertFalse(self.listing.featured)
    
    def test_location_text(self):
        """Test location_text method"""
        expected = "London, United Kingdom"
        self.assertEqual(self.listing.location_text(), expected)
    
    def test_listing_str(self):
        """Test string representation"""
        self.assertEqual(str(self.listing), "The Accessible Cafe")
    
    def test_listing_defaults(self):
        """Test default values"""
        listing = Listing.objects.create(
            name="Test Venue",
            city="Paris",
            country="France"
        )
        self.assertEqual(listing.categories, [])
        self.assertEqual(listing.photos, [])
        self.assertEqual(listing.accessibility_features, [])
        self.assertEqual(listing.tags, [])
        self.assertEqual(listing.opening_hours, {})
    
    def test_get_accessibility_badges_no_reviews(self):
        """Test accessibility badges with no reviews"""
        badges = self.listing.get_accessibility_badges()
        self.assertEqual(badges, [])
    
    def test_get_accessibility_badges_with_reviews(self):
        """Test accessibility badges with high-rated reviews"""
        # Create approved reviews with high accessibility scores
        Review.objects.create(
            listing=self.listing,
            author_name="John Doe",
            rating=5,
            step_free_access=5,
            restroom_accessible=5,
            moderation_status="approved"
        )
        Review.objects.create(
            listing=self.listing,
            author_name="Jane Smith",
            rating=4,
            step_free_access=4,
            restroom_accessible=4,
            moderation_status="approved"
        )
        
        badges = self.listing.get_accessibility_badges()
        self.assertGreater(len(badges), 0)
        # Check that step-free access badge is present
        badge_labels = [b['label'] for b in badges]
        self.assertIn("Step-Free Access", badge_labels)
    
    def test_has_photos_property(self):
        """Test has_photos property"""
        self.assertFalse(self.listing.has_photos)


class ListingPhotoModelTest(TestCase):
    """Test ListingPhoto model"""
    
    def setUp(self):
        self.listing = Listing.objects.create(
            name="Test Venue",
            city="London",
            country="UK"
        )
    
    def test_photo_str(self):
        """Test string representation"""
        photo = ListingPhoto.objects.create(
            listing=self.listing,
            caption="Main entrance"
        )
        self.assertEqual(str(photo), "Photo for Test Venue")
    
    def test_primary_photo_exclusivity(self):
        """Test that only one photo can be primary at a time"""
        photo1 = ListingPhoto.objects.create(
            listing=self.listing,
            is_primary=True
        )
        photo2 = ListingPhoto.objects.create(
            listing=self.listing,
            is_primary=True
        )
        
        # Refresh photo1 from database
        photo1.refresh_from_db()
        
        # Only photo2 should be primary now
        self.assertFalse(photo1.is_primary)
        self.assertTrue(photo2.is_primary)


class ReviewModelTest(TestCase):
    """Test Review model and rating signals"""
    
    def setUp(self):
        self.listing = Listing.objects.create(
            name="Test Restaurant",
            city="London",
            country="UK"
        )
    
    def test_review_creation(self):
        """Test basic review creation"""
        review = Review.objects.create(
            listing=self.listing,
            author_name="Alice",
            author_email="alice@example.com",
            rating=4,
            comment="Great place!",
            step_free_access=5,
            moderation_status="approved"
        )
        self.assertEqual(review.rating, 4)
        self.assertEqual(str(review), "Alice - Test Restaurant (4★)")
    
    def test_review_rating_validation(self):
        """Test rating validation (1-5 scale)"""
        with self.assertRaises(ValidationError):
            review = Review(
                listing=self.listing,
                author_name="Bob",
                rating=6  # Invalid rating
            )
            review.full_clean()
    
    def test_listing_rating_auto_update_on_save(self):
        """Test that listing rating updates when review is saved"""
        Review.objects.create(
            listing=self.listing,
            author_name="User1",
            rating=4,
            moderation_status="approved"
        )
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.rating, 4.0)
        self.assertEqual(self.listing.reviews_count, 1)
        
        Review.objects.create(
            listing=self.listing,
            author_name="User2",
            rating=5,
            moderation_status="approved"
        )
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.rating, 4.5)
        self.assertEqual(self.listing.reviews_count, 2)
    
    def test_listing_rating_ignores_pending_reviews(self):
        """Test that pending reviews don't affect rating"""
        Review.objects.create(
            listing=self.listing,
            author_name="User1",
            rating=5,
            moderation_status="approved"
        )
        Review.objects.create(
            listing=self.listing,
            author_name="User2",
            rating=1,
            moderation_status="pending"
        )
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.rating, 5.0)
        self.assertEqual(self.listing.reviews_count, 1)
    
    def test_listing_rating_auto_update_on_delete(self):
        """Test that listing rating updates when review is deleted"""
        review1 = Review.objects.create(
            listing=self.listing,
            author_name="User1",
            rating=3,
            moderation_status="approved"
        )
        review2 = Review.objects.create(
            listing=self.listing,
            author_name="User2",
            rating=5,
            moderation_status="approved"
        )
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.rating, 4.0)
        
        review1.delete()
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.rating, 5.0)
        self.assertEqual(self.listing.reviews_count, 1)


class TeamMemberModelTest(TestCase):
    """Test TeamMember model"""
    
    def test_team_member_creation(self):
        """Test basic team member creation"""
        member = TeamMember.objects.create(
            name="John Doe",
            role="Founder",
            bio="<p>Passionate about accessibility</p>",
            order=1
        )
        self.assertEqual(str(member), "John Doe - Founder")
        self.assertTrue(member.is_active)
    
    def test_team_member_ordering(self):
        """Test team members are ordered by order field"""
        member1 = TeamMember.objects.create(name="Alice", role="CEO", order=2)
        member2 = TeamMember.objects.create(name="Bob", role="CTO", order=1)
        members = TeamMember.objects.all()
        self.assertEqual(members[0].name, "Bob")


class PartnerModelTest(TestCase):
    """Test Partner model"""
    
    def test_partner_creation(self):
        """Test basic partner creation"""
        partner = Partner.objects.create(
            name="AccessTech Inc",
            type="sponsor",
            description="<p>Technology for accessibility</p>",
            order=1
        )
        self.assertEqual(str(partner), "AccessTech Inc (Sponsor)")
        self.assertTrue(partner.is_active)


class ContactMessageModelTest(TestCase):
    """Test ContactMessage model"""
    
    def test_contact_message_creation(self):
        """Test basic contact message creation"""
        message = ContactMessage.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            subject="Question about accessibility",
            message="I have a question..."
        )
        self.assertEqual(str(message), "Message from Jane Doe (jane@example.com)")
        self.assertFalse(message.is_read)


class BlogCategoryModelTest(TestCase):
    """Test BlogCategory model"""
    
    def test_blog_category_creation(self):
        """Test basic blog category creation"""
        category = BlogCategory.objects.create(
            name="Travel Tips",
            slug="travel-tips"
        )
        self.assertEqual(str(category), "Travel Tips")


class BlogPostModelTest(TestCase):
    """Test BlogPost model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123"
        )
        self.category = BlogCategory.objects.create(
            name="News",
            slug="news"
        )
    
    def test_blog_post_creation(self):
        """Test basic blog post creation"""
        post = BlogPost.objects.create(
            title="Accessible Travel in 2026",
            slug="accessible-travel-2026",
            category=self.category,
            author=self.user,
            content="<p>Great tips for accessible travel...</p>",
            excerpt="Travel tips for 2026"
        )
        self.assertEqual(str(post), "Accessible Travel in 2026")
        self.assertTrue(post.is_published)


class SponsorshipPackageModelTest(TestCase):
    """Test SponsorshipPackage model"""
    
    def test_sponsorship_package_creation(self):
        """Test basic sponsorship package creation"""
        package = SponsorshipPackage.objects.create(
            name="Gold Sponsor",
            slug="gold",
            price=Decimal("5000.00"),
            period="Yearly",
            features=["Logo on website", "Social media mentions"],
            order=1
        )
        self.assertEqual(str(package), "Gold Sponsor")
        self.assertTrue(package.is_active)


class DonationGoalModelTest(TestCase):
    """Test DonationGoal model"""
    
    def test_donation_goal_creation(self):
        """Test basic donation goal creation"""
        goal = DonationGoal.objects.create(
            title="New Website Features",
            slug="new-features",
            description="<p>Help us build new features</p>",
            target_amount=Decimal("10000.00"),
            raised_amount=Decimal("2500.00")
        )
        self.assertEqual(str(goal), "New Website Features")
        self.assertTrue(goal.is_active)
