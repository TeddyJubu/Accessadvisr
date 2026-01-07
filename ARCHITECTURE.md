# 🏛️ Architecture & Code Organization

**Understanding how AccessAdvisr is structured**

---

## 📐 System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Browser │  │  Mobile  │  │   API    │  │  Admin   │   │
│  │   User   │  │   User   │  │  Client  │  │   User   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │      LOAD BALANCER          │
        │    (Google Cloud Run)       │
        └─────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Django Application                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │   Views    │  │   Models   │  │  Templates │     │  │
│  │  │ (Business  │  │ (Database  │  │   (HTML)   │     │  │
│  │  │   Logic)   │  │   Layer)   │  │            │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  │                                                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │   Forms    │  │   Utils    │  │   Signals  │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │  Static Files│  │    Cache     │     │
│  │  (Database)  │  │ (WhiteNoise) │  │   (Redis)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Google Maps  │  │   Geocoding  │  │    Places    │     │
│  │  JavaScript  │  │      API     │  │     API      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### 1. User Visits Homepage

```
User Browser
    │
    ├─→ GET /
    │
    ▼
Django URL Router (accessadvisr/urls.py)
    │
    ├─→ Route to core.urls
    │
    ▼
Core URL Router (core/urls.py)
    │
    ├─→ Match pattern '' → views.home
    │
    ▼
View Function (core/views.py::home)
    │
    ├─→ Query: Listing.objects.filter(featured=True)
    │
    ▼
Database (PostgreSQL/SQLite)
    │
    ├─→ Return featured listings
    │
    ▼
Template Rendering (templates/core/home.html)
    │
    ├─→ Include partials (hero_map, search_bar, etc.)
    ├─→ Inject GOOGLE_MAPS_BROWSER_KEY via context processor
    │
    ▼
HTTP Response (HTML)
    │
    └─→ Browser renders page
         │
         └─→ JavaScript loads Google Maps
              │
              └─→ Fetch /api/listings/ (AJAX)
                   │
                   └─→ Add markers to map
```

### 2. User Searches for Venues

```
User enters "museum" in search box
    │
    ├─→ Submit form (GET /listings/?q=museum)
    │
    ▼
View Function (core/views.py::listings_list)
    │
    ├─→ Parse query parameters (q, category, location)
    ├─→ Filter queryset: Listing.objects.filter(name__icontains='museum')
    ├─→ Paginate results (12 per page)
    │
    ▼
Template Rendering (templates/core/listings_list.html)
    │
    └─→ Display filtered results with pagination
```

### 3. User Submits Review

```
User fills review form
    │
    ├─→ POST /listing/5/review/
    │
    ▼
View Function (core/views.py::submit_review)
    │
    ├─→ Validate form (ReviewForm)
    ├─→ Create Review object (status=pending)
    ├─→ Save to database
    │
    ▼
Django Signal (post_save)
    │
    ├─→ Trigger: update_listing_rating_on_save
    ├─→ Calculate average rating from approved reviews
    ├─→ Update Listing.rating and Listing.reviews_count
    │
    ▼
Redirect to success page
```

---

## 📦 Module Breakdown

### Core App (`core/`)

#### **models.py** - Data Models

```python
# Three main models:

1. Category
   - Organizes listings into categories
   - Stores marker styling (icon, color)

2. Listing
   - Represents an accessible venue
   - Contains location, contact, accessibility info
   - Auto-computed rating from reviews

3. Review
   - User-submitted accessibility review
   - Detailed accessibility ratings (1-5 scale)
   - Moderation workflow (pending → approved/rejected)
```

**Key Relationships:**

```
Category (1) ────────────── (N) Listing
                                   │
                                   │ (1)
                                   │
                                   ▼
                                  (N) Review
```

#### **views.py** - Business Logic

```python
# Public Views
home()                    # Homepage with featured listings
listings_list()           # Paginated venue list with filters
listing_detail()          # Single venue detail page
submit_review()           # Handle review submission
submit_listing()          # User-submitted venue form

# Admin Views
admin_page()              # Moderation dashboard
admin_moderate()          # Approve/reject actions

# API Views
listings_api()            # JSON endpoint for map markers
```

#### **forms.py** - Form Definitions

```python
ReviewForm                # Review submission form
ListingSubmissionForm     # User-submitted venue form
```

#### **utils.py** - Utility Functions

```python
geocode_listing()         # Convert address → lat/lng using Google API
```

#### **context_processors.py** - Global Template Context

```python
google_maps_key()         # Inject GOOGLE_MAPS_BROWSER_KEY into all templates
```

#### **admin.py** - Django Admin Configuration

```python
# Customizes Django admin interface for:
- Listing management
- Review moderation
- Category management
```

#### **urls.py** - URL Routing

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings_list, name='listings_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    # ... more routes
]
```

---

## 🗂️ Template Organization

### Template Hierarchy

```
templates/
│
├── base.html                      # Global layout
│   ├── Header (logo, nav)
│   ├── {% block content %}
│   └── Footer (scripts)
│
└── core/
    ├── home.html                  # Homepage
    │   ├── {% extends "base.html" %}
    │   └── {% include "core/partials/..." %}
    │
    ├── listings_list.html         # Venue list
    ├── listing_detail.html        # Venue detail
    ├── submit_listing.html        # Add venue form
    ├── admin.html                 # Admin dashboard
    │
    └── partials/                  # Reusable components
        ├── hero_map.html          # Map container
        ├── search_bar.html        # Search interface
        ├── explore_cards.html     # Featured cards
        ├── stats.html             # Statistics section
        ├── contributions.html     # Recent contributions
        ├── testimonial.html       # Testimonial slider
        ├── footer.html            # Footer
        ├── back_to_top.html       # Back to top button
        └── scripts.html           # JavaScript (map init, API calls)
```

### Template Inheritance Example

```django
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}AccessAdvisr{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <header>...</header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>

{# home.html #}
{% extends "base.html" %}

{% block title %}AccessAdvisr — Home{% endblock %}

{% block content %}
    {% include "core/partials/hero_map.html" %}
    {% include "core/partials/search_bar.html" %}
    {% include "core/partials/explore_cards.html" %}
{% endblock %}
```

---

## 🔌 API Architecture

### RESTful Endpoints

```
GET  /api/listings/              # List all approved listings
     ?q=museum                   # Filter by keyword
     &category=Entertainment     # Filter by category
     &location=London            # Filter by location
```

### Response Format

```json
{
  "listings": [
    {
      "id": 1,
      "name": "British Museum",
      "subtitle": "World-class museum",
      "lat": 51.5194,
      "lng": -0.1270,
      "rating": 4.8,
      "reviews_count": 42,
      "categories": ["Entertainment", "Culture"],
      "accessibility_features": ["wheelchair", "braille"],
      "status": "open",
      "city": "London",
      "country": "United Kingdom"
    }
  ]
}
```

### API Flow

```
JavaScript (scripts.html)
    │
    ├─→ fetch('/api/listings/?location=London')
    │
    ▼
Django View (listings_api)
    │
    ├─→ Parse query params
    ├─→ Filter Listing.objects
    ├─→ Serialize to JSON
    │
    ▼
JSON Response
    │
    └─→ JavaScript processes data
         │
         └─→ Add markers to Google Map
```

---

## 🗄️ Database Design

### Schema Diagram

```sql
-- Category Table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(50) DEFAULT 'map-pin',
    color VARCHAR(7) DEFAULT '#FF431E'
);

-- Listing Table
CREATE TABLE listing (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    subtitle VARCHAR(200),
    description TEXT,
    categories JSONB DEFAULT '[]',
    city VARCHAR(120) NOT NULL,
    country VARCHAR(120) NOT NULL,
    address VARCHAR(255),
    lat FLOAT,
    lng FLOAT,
    phone VARCHAR(40),
    website VARCHAR(200),
    email VARCHAR(254),
    price_min INTEGER,
    price_max INTEGER,
    opening_hours JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'open',
    photos JSONB DEFAULT '[]',
    accessibility_features JSONB DEFAULT '[]',
    rating FLOAT DEFAULT 0,
    reviews_count INTEGER DEFAULT 0,
    tags JSONB DEFAULT '[]',
    featured BOOLEAN DEFAULT FALSE,
    moderation_status VARCHAR(20) DEFAULT 'approved',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Review Table
CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER REFERENCES listing(id) ON DELETE CASCADE,
    author_name VARCHAR(100) NOT NULL,
    author_email VARCHAR(254),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    step_free_access INTEGER CHECK (step_free_access >= 1 AND step_free_access <= 5),
    restroom_accessible INTEGER CHECK (restroom_accessible >= 1 AND restroom_accessible <= 5),
    signage_clear INTEGER CHECK (signage_clear >= 1 AND signage_clear <= 5),
    staff_supportive INTEGER CHECK (staff_supportive >= 1 AND staff_supportive <= 5),
    sensory_friendly INTEGER CHECK (sensory_friendly >= 1 AND sensory_friendly <= 5),
    moderation_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_listing_city ON listing(city);
CREATE INDEX idx_listing_country ON listing(country);
CREATE INDEX idx_listing_rating ON listing(rating);
CREATE INDEX idx_listing_moderation ON listing(moderation_status);
CREATE INDEX idx_review_listing ON review(listing_id);
CREATE INDEX idx_review_moderation ON review(moderation_status);
```

### Query Optimization

```python
# Bad: N+1 query problem
for listing in Listing.objects.all():
    print(listing.reviews.count())  # Queries database for each listing!

# Good: Use aggregation
from django.db.models import Count
listings = Listing.objects.annotate(review_count=Count('reviews'))
for listing in listings:
    print(listing.review_count)  # No additional queries!

# Good: Use select_related for foreign keys
reviews = Review.objects.select_related('listing').all()

# Good: Use prefetch_related for reverse foreign keys
listings = Listing.objects.prefetch_related('reviews').all()
```

---

## 🔐 Security Architecture

### Authentication Flow

```
User Login Request
    │
    ├─→ POST /login/
    │
    ▼
Django Authentication
    │
    ├─→ Validate credentials
    ├─→ Create session
    ├─→ Set session cookie (httpOnly, secure)
    │
    ▼
Redirect to dashboard
```

### Security Layers

1. **CSRF Protection** - Django middleware validates CSRF tokens
2. **SQL Injection Prevention** - Django ORM parameterizes queries
3. **XSS Prevention** - Django templates auto-escape HTML
4. **Session Security** - Secure cookies in production
5. **Environment Variables** - Secrets stored in `.env`

### API Key Security

```python
# Browser Key (client-side)
# Restricted by HTTP referrer
# Can be seen in browser, but restricted to your domain

# Server Key (server-side)
# Restricted by IP address
# Never exposed to client
# Used only in backend geocoding
```

---

## 🚀 Deployment Architecture

### Production Stack

```
┌─────────────────────────────────────────┐
│         Google Cloud Run                │
│  ┌───────────────────────────────────┐  │
│  │  Container Instance 1             │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Gunicorn (WSGI Server)     │  │  │
│  │  │  ├─→ Worker 1               │  │  │
│  │  │  ├─→ Worker 2               │  │  │
│  │  │  └─→ Worker 3               │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │  Container Instance 2 (Auto-scale)│  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│      Cloud SQL (PostgreSQL)             │
└─────────────────────────────────────────┘
```

### Docker Container

```dockerfile
FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with Gunicorn
CMD exec gunicorn --bind :$PORT --workers 3 --threads 8 accessadvisr.wsgi:application
```

---

## 📊 Performance Optimization

### Caching Strategy

```python
# View-level caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def listings_api(request):
    # ...

# Template fragment caching
{% load cache %}
{% cache 500 sidebar %}
    ... expensive sidebar content ...
{% endcache %}

# Database query caching
from django.core.cache import cache

def get_featured_listings():
    listings = cache.get('featured_listings')
    if not listings:
        listings = Listing.objects.filter(featured=True)[:6]
        cache.set('featured_listings', listings, 60 * 30)  # 30 min
    return listings
```

### Database Optimization

```python
# Use select_related for foreign keys
Review.objects.select_related('listing').all()

# Use prefetch_related for reverse foreign keys
Listing.objects.prefetch_related('reviews').all()

# Use only() to fetch specific fields
Listing.objects.only('id', 'name', 'lat', 'lng')

# Use defer() to exclude heavy fields
Listing.objects.defer('description', 'opening_hours')

# Use values() for dictionaries (faster than model instances)
Listing.objects.values('id', 'name', 'rating')
```

---

## 🧪 Testing Architecture

### Test Structure

```
core/tests/
├── __init__.py
├── test_models.py        # Model tests
├── test_views.py         # View tests
├── test_forms.py         # Form tests
├── test_utils.py         # Utility function tests
└── test_api.py           # API endpoint tests
```

### Example Tests

```python
# test_models.py
from django.test import TestCase
from core.models import Listing, Review

class ListingModelTest(TestCase):
    def test_rating_calculation(self):
        listing = Listing.objects.create(name="Test Venue")
        Review.objects.create(
            listing=listing,
            rating=5,
            moderation_status='approved'
        )
        listing.refresh_from_db()
        self.assertEqual(listing.rating, 5.0)
        self.assertEqual(listing.reviews_count, 1)

# test_views.py
from django.test import TestCase, Client

class ViewsTest(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AccessAdvisr')

# test_api.py
class APITest(TestCase):
    def test_listings_api(self):
        response = self.client.get('/api/listings/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('listings', data)
```

---

## 📈 Monitoring & Logging

### Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Usage in Code

```python
import logging

logger = logging.getLogger(__name__)

def geocode_listing(listing):
    try:
        # Geocoding logic
        pass
    except Exception as e:
        logger.error(f"Geocoding failed for {listing.name}: {e}")
        return False
```

---

## 🎯 Best Practices Summary

### Code Organization
- ✅ Keep views focused (single responsibility)
- ✅ Use Django's built-in features
- ✅ Separate business logic into utils
- ✅ Use template partials for reusability

### Performance
- ✅ Use database indexes
- ✅ Implement caching
- ✅ Optimize queries (select_related, prefetch_related)
- ✅ Paginate large datasets

### Security
- ✅ Never commit secrets
- ✅ Use environment variables
- ✅ Enable CSRF protection
- ✅ Validate user input

### Maintainability
- ✅ Write tests
- ✅ Document code
- ✅ Use meaningful variable names
- ✅ Follow PEP 8 style guide

---

**This architecture is designed for scalability, maintainability, and accessibility-first principles.**
