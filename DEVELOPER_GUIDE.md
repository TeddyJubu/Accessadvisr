# 🚀 AccessAdvisr - Complete Developer Guide

**A comprehensive guide for junior developers to understand and recreate this project from scratch.**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [Setup Guide](#setup-guide)
7. [Feature Implementation](#feature-implementation)
8. [API Documentation](#api-documentation)
9. [Deployment Guide](#deployment-guide)
10. [Testing & Quality Assurance](#testing--quality-assurance)
11. [Common Issues & Solutions](#common-issues--solutions)
12. [Best Practices](#best-practices)

---

## 🎯 Project Overview

### What is AccessAdvisr?

AccessAdvisr is a **community-powered accessibility directory** that helps disabled travelers discover, evaluate, and share real-world access information about venues worldwide.

### Core Features

- 🗺️ **Interactive Google Maps** with 49+ real London venues
- ♿ **Accessibility-First** design with detailed accessibility reviews
- 🔍 **Smart Search & Filtering** by category, location, and keywords
- 📱 **Responsive Design** that works on all devices
- ⭐ **Review System** with accessibility-specific ratings
- 🏛️ **Real Venues** including museums, restaurants, hotels, attractions, and more
- 🚀 **Production Ready** deployed on Google Cloud Run

### Target Users

1. **Disabled travelers** seeking accessible venues
2. **Allies** who want to contribute accessibility information
3. **Venue owners** who want to showcase their accessibility features

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Django** | 6.0 | Web framework (MVT pattern) |
| **SQLite** | 3.x | Development database |
| **PostgreSQL** | 14+ | Production database (via DATABASE_URL) |
| **Gunicorn** | 23.0.0 | WSGI HTTP server for production |
| **WhiteNoise** | 6.8.2 | Static file serving |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic markup |
| **Tailwind CSS** | Utility-first CSS framework (CDN) |
| **Lucide Icons** | Icon library |
| **Vanilla JavaScript** | Client-side interactivity |
| **Google Maps JavaScript API** | Interactive maps |

### External APIs

- **Google Maps JavaScript API** - Map rendering
- **Google Places API** - Location autocomplete
- **Google Geocoding API** - Address → Coordinates conversion

### DevOps & Deployment

- **Docker** - Containerization
- **Google Cloud Run** - Serverless deployment
- **Git** - Version control
- **python-dotenv** - Environment variable management

---

## 🏗️ Architecture & Design Patterns

### Django MVT Pattern

AccessAdvisr follows Django's **Model-View-Template (MVT)** architecture:

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│    URLs     │ ← Route matching (urls.py)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Views    │ ← Business logic (views.py)
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐ ┌─────────────┐
│   Models    │ │  Templates  │
│ (Database)  │ │   (HTML)    │
└─────────────┘ └─────────────┘
```

### Key Design Patterns

1. **Model-View-Template (MVT)** - Django's core pattern
2. **Repository Pattern** - Django ORM abstracts database operations
3. **Signal Pattern** - Auto-update ratings when reviews change
4. **Context Processors** - Inject Google Maps keys globally
5. **Management Commands** - Custom CLI commands for data seeding

### Application Flow

```
User Request → URL Router → View Function → Model Query → Template Render → HTTP Response
```

---

## 📁 Project Structure

```
Accessadvisr/
│
├── 📂 accessadvisr/              # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # ⚙️ Project settings (database, static files, etc.)
│   ├── urls.py                   # 🔗 Root URL configuration
│   ├── wsgi.py                   # 🌐 WSGI entry point for production
│   └── asgi.py                   # 🌐 ASGI entry point (async support)
│
├── 📂 core/                      # Main application
│   ├── __init__.py
│   ├── models.py                 # 🗄️ Database models (Listing, Review, Category)
│   ├── views.py                  # 🎯 View functions (business logic)
│   ├── urls.py                   # 🔗 App-specific URL patterns
│   ├── admin.py                  # 🔧 Django admin configuration
│   ├── forms.py                  # 📝 Form definitions
│   ├── utils.py                  # 🛠️ Utility functions (geocoding)
│   ├── context_processors.py    # 🔑 Global template context
│   ├── tests.py                  # ✅ Unit tests
│   │
│   ├── 📂 management/commands/   # Custom Django commands
│   │   ├── seed_listings.py      # 🌱 Seed sample data
│   │   ├── seed_london_venues.py # 🌱 Seed 49 London venues
│   │   ├── geocode_listings.py   # 📍 Add GPS coordinates
│   │   └── fetch_london_data.py  # 📡 Fetch real venue data
│   │
│   └── 📂 migrations/            # Database migrations
│       ├── 0001_initial.py
│       └── 0002_category_alter_listing_options_and_more.py
│
├── 📂 templates/                 # HTML templates
│   ├── base.html                 # 🎨 Base layout (header, footer)
│   │
│   ├── 📂 core/
│   │   ├── home.html             # 🏠 Homepage
│   │   ├── listings_list.html    # 📋 Venue listing page
│   │   ├── listing_detail.html   # 📄 Single venue detail
│   │   ├── submit_listing.html   # ➕ Add new venue form
│   │   ├── admin.html            # 🔧 Admin dashboard
│   │   │
│   │   └── 📂 partials/          # Reusable template components
│   │       ├── hero_map.html     # 🗺️ Map hero section
│   │       ├── search_bar.html   # 🔍 Search interface
│   │       ├── explore_cards.html
│   │       ├── stats.html
│   │       ├── contributions.html
│   │       ├── testimonial.html
│   │       ├── footer.html
│   │       ├── back_to_top.html
│   │       └── scripts.html      # 📜 JavaScript (map init, API calls)
│   │
│   └── 📂 registration/          # Auth templates
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
├── 📂 static/                    # Static assets (if any)
├── 📂 staticfiles/               # Collected static files (production)
│
├── 📂 dataconnect/               # Firebase Data Connect (optional)
├── 📂 .firebase/                 # Firebase config
│
├── 📄 manage.py                  # Django management script
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env                       # 🔐 Environment variables (DO NOT COMMIT!)
├── 📄 .env.example               # Template for .env
├── 📄 .gitignore                 # Git ignore rules
├── 📄 Dockerfile                 # Docker container definition
├── 📄 entrypoint.sh              # Docker entrypoint script
├── 📄 firebase.json              # Firebase configuration
├── 📄 .firebaserc               # Firebase project settings
│
├── 📄 db.sqlite3                 # SQLite database (development)
│
└── 📄 Documentation/
    ├── README.md                 # Quick start guide
    ├── DEVELOPER_GUIDE.md        # This file
    ├── GOOGLE_MAPS_SETUP.md      # Google Maps API setup
    ├── DEVELOPMENT_WORKFLOW.md   # Development workflow
    ├── IMPLEMENTATION_SUMMARY.md # Feature implementation summary
    ├── LONDON_VENUES_UPDATE.md   # London venues data
    └── TECHNICAL_HANDOFF.md      # Technical handoff notes
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│    Category     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ slug            │
│ icon            │
│ color           │
└─────────────────┘

┌─────────────────────────────┐
│         Listing             │
├─────────────────────────────┤
│ id (PK)                     │
│ name                        │
│ subtitle                    │
│ description                 │
│ categories (JSON)           │
│ city                        │
│ country                     │
│ address                     │
│ lat, lng                    │
│ phone, website, email       │
│ price_min, price_max        │
│ opening_hours (JSON)        │
│ status                      │
│ photos (JSON)               │
│ accessibility_features (JSON)│
│ rating (computed)           │
│ reviews_count (computed)    │
│ tags (JSON)                 │
│ featured                    │
│ moderation_status           │
│ created_at, updated_at      │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────────────┐
│          Review             │
├─────────────────────────────┤
│ id (PK)                     │
│ listing_id (FK)             │
│ author_name                 │
│ author_email                │
│ rating (1-5)                │
│ comment                     │
│ step_free_access (1-5)      │
│ restroom_accessible (1-5)   │
│ signage_clear (1-5)         │
│ staff_supportive (1-5)      │
│ sensory_friendly (1-5)      │
│ moderation_status           │
│ created_at, updated_at      │
└─────────────────────────────┘
```

### Models Explained

#### 1. **Category Model**

Organizes listings into categories with custom marker styling.

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="map-pin")  # Lucide icon
    color = models.CharField(max_length=7, default="#FF431E")  # Hex color
```

**Example Categories:**
- Accommodation (🏨)
- Food & Restaurants (🍽️)
- Entertainment (🎭)
- Sport & Recreational (⚽)

#### 2. **Listing Model**

Represents an accessible venue with detailed information.

**Key Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField | Venue name |
| `categories` | JSONField | List of category names |
| `lat`, `lng` | FloatField | GPS coordinates |
| `accessibility_features` | JSONField | Quick tags (wheelchair, braille, etc.) |
| `rating` | FloatField | Auto-computed from reviews |
| `moderation_status` | CharField | pending/approved/rejected |

**JSON Fields:**

```python
# categories example
["Food & Restaurants", "Entertainment"]

# accessibility_features example
["wheelchair", "braille", "hearing_loop", "accessible_parking"]

# opening_hours example
{
    "monday": "9:00-17:00",
    "tuesday": "9:00-17:00",
    "wednesday": "Closed",
    ...
}

# photos example
["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"]
```

#### 3. **Review Model**

User-submitted accessibility reviews with detailed ratings.

**Accessibility Rating Fields (1-5 scale):**
- `step_free_access` - Wheelchair accessibility
- `restroom_accessible` - Accessible restrooms
- `signage_clear` - Clear signage
- `staff_supportive` - Helpful staff
- `sensory_friendly` - Lighting, noise levels

**Auto-Rating System:**

When a review is saved/deleted, Django signals automatically recalculate the listing's overall rating:

```python
@receiver(post_save, sender=Review)
def update_listing_rating_on_save(sender, instance, **kwargs):
    listing = instance.listing
    approved_reviews = listing.reviews.filter(moderation_status="approved")
    avg_rating = approved_reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    listing.rating = round(avg_rating, 1)
    listing.reviews_count = approved_reviews.count()
    listing.save(update_fields=["rating", "reviews_count"])
```

---

## 🚀 Setup Guide

### Prerequisites

- **Python 3.10+** installed
- **pip** (Python package manager)
- **Git** for version control
- **Google Cloud account** (for Maps API)
- **Code editor** (VS Code recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/TeddyJubu/Accessadvisr.git
cd Accessadvisr
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies explained:**

```txt
Django==6.0                 # Web framework
gunicorn==23.0.0           # Production server
whitenoise==6.8.2          # Static file serving
psycopg2-binary==2.9.10    # PostgreSQL adapter
dj-database-url==2.3.0     # Database URL parsing
python-dotenv==1.2.1       # Environment variables
requests==2.32.5           # HTTP library (for geocoding)
django-cors-headers==4.6.0 # CORS handling
```

### Step 4: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

**Required environment variables:**

```bash
# Google Maps API Keys
GOOGLE_MAPS_BROWSER_KEY=your_browser_key_here
GOOGLE_MAPS_SERVER_KEY=your_server_key_here

# Django Settings
DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
PRODUCTION=False

# Database (optional, defaults to SQLite)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
```

**How to get Google Maps API keys:**

See `GOOGLE_MAPS_SETUP.md` for detailed instructions. Quick summary:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Create two API keys:
   - **Browser key** (restricted by HTTP referrer)
   - **Server key** (restricted by IP address)

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

This creates the database tables based on your models.

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 7: Seed Sample Data

```bash
# Option 1: Seed 5 sample venues
python manage.py seed_listings

# Option 2: Seed 49 real London venues (recommended)
python manage.py seed_london_venues
```

### Step 8: Geocode Listings

Add GPS coordinates to venues:

```bash
python manage.py geocode_listings
```

### Step 9: Collect Static Files (Production)

```bash
python manage.py collectstatic --noinput
```

### Step 10: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 💡 Feature Implementation

### 1. Google Maps Integration

**Files involved:**
- `templates/core/partials/hero_map.html` - Map container
- `templates/core/partials/scripts.html` - Map initialization
- `core/context_processors.py` - Inject API key
- `accessadvisr/settings.py` - Configure context processor

**How it works:**

1. **Context Processor** injects the API key into all templates:

```python
# core/context_processors.py
def google_maps_key(request):
    return {
        'GOOGLE_MAPS_BROWSER_KEY': settings.GOOGLE_MAPS_BROWSER_KEY
    }
```

2. **Base Template** loads Google Maps API:

```html
<!-- templates/base.html -->
<script src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_BROWSER_KEY }}&libraries=places,marker&loading=async"></script>
```

3. **Map Initialization** in `scripts.html`:

```javascript
let map;
let markers = [];

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  
  map = new Map(document.getElementById("map"), {
    center: { lat: 51.5074, lng: -0.1278 }, // London
    zoom: 12,
    mapId: "DEMO_MAP_ID"
  });
  
  // Fetch listings and add markers
  fetchListings();
}
```

4. **API Endpoint** returns listings as JSON:

```python
# core/views.py
def listings_api(request):
    listings = Listing.objects.filter(moderation_status="approved")
    
    # Apply filters
    q = request.GET.get('q')
    if q:
        listings = listings.filter(
            Q(name__icontains=q) | Q(subtitle__icontains=q)
        )
    
    data = {
        "listings": [
            {
                "id": listing.id,
                "name": listing.name,
                "lat": listing.lat,
                "lng": listing.lng,
                # ... more fields
            }
            for listing in listings
        ]
    }
    return JsonResponse(data)
```

### 2. Search & Filtering

**Search by:**
- Keywords (name, subtitle)
- Category
- Location (city, country)

**Implementation:**

```python
# core/views.py
def listings_list(request):
    listings = Listing.objects.filter(moderation_status="approved")
    
    # Keyword search
    q = request.GET.get('q')
    if q:
        listings = listings.filter(
            Q(name__icontains=q) | Q(subtitle__icontains=q)
        )
    
    # Category filter
    category = request.GET.get('category')
    if category:
        listings = listings.filter(categories__contains=[category])
    
    # Location filter
    location = request.GET.get('location')
    if location:
        listings = listings.filter(
            Q(city__icontains=location) | Q(country__icontains=location)
        )
    
    # Pagination
    paginator = Paginator(listings, 12)
    page = request.GET.get('page')
    listings = paginator.get_page(page)
    
    return render(request, 'core/listings_list.html', {'listings': listings})
```

### 3. Geocoding System

**Purpose:** Convert addresses to GPS coordinates (lat/lng).

**How it works:**

1. **Utility Function** (`core/utils.py`):

```python
import requests
from django.conf import settings

def geocode_listing(listing):
    """Geocode a listing using Google Geocoding API"""
    if listing.lat and listing.lng:
        return True  # Already geocoded
    
    # Build address string
    address_parts = [listing.address, listing.city, listing.country]
    address = ", ".join(filter(None, address_parts))
    
    # Call Google Geocoding API
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": settings.GOOGLE_MAPS_SERVER_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        listing.lat = location['lat']
        listing.lng = location['lng']
        listing.save(update_fields=['lat', 'lng'])
        return True
    
    return False
```

2. **Management Command** (`core/management/commands/geocode_listings.py`):

```python
from django.core.management.base import BaseCommand
from core.models import Listing
from core.utils import geocode_listing

class Command(BaseCommand):
    help = 'Geocode all listings without coordinates'
    
    def handle(self, *args, **options):
        listings = Listing.objects.filter(lat__isnull=True)
        
        for listing in listings:
            success = geocode_listing(listing)
            if success:
                self.stdout.write(f"✓ {listing.name}")
            else:
                self.stdout.write(f"✗ {listing.name}")
```

**Usage:**

```bash
python manage.py geocode_listings
```

### 4. Review System

**Features:**
- Overall rating (1-5 stars)
- Accessibility-specific ratings
- Moderation system
- Auto-update listing ratings

**Submission Flow:**

```
User fills form → POST to /listing/<id>/review/ → Create Review (pending)
                                                  ↓
                                          Admin approves
                                                  ↓
                                          Signal fires
                                                  ↓
                                    Listing rating recalculated
```

**Form Implementation:**

```python
# core/forms.py
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'author_name', 'author_email', 'rating', 'comment',
            'step_free_access', 'restroom_accessible', 'signage_clear',
            'staff_supportive', 'sensory_friendly'
        ]
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
```

**View Implementation:**

```python
# core/views.py
def submit_review(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.moderation_status = 'pending'
            review.save()
            return redirect('review_success', pk=listing.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'core/listing_detail.html', {
        'listing': listing,
        'form': form
    })
```

### 5. Admin Dashboard

**Features:**
- Moderation queue for listings and reviews
- Approve/reject actions
- Statistics overview

**Implementation:**

```python
# core/views.py
def admin_page(request):
    pending_listings = Listing.objects.filter(moderation_status='pending')
    pending_reviews = Review.objects.filter(moderation_status='pending')
    
    stats = {
        'total_listings': Listing.objects.filter(moderation_status='approved').count(),
        'total_reviews': Review.objects.filter(moderation_status='approved').count(),
        'pending_listings': pending_listings.count(),
        'pending_reviews': pending_reviews.count(),
    }
    
    return render(request, 'core/admin.html', {
        'pending_listings': pending_listings,
        'pending_reviews': pending_reviews,
        'stats': stats
    })
```

---

## 📡 API Documentation

### Base URL

```
http://127.0.0.1:8000/api/
```

### Endpoints

#### 1. **GET /api/listings/**

Fetch all approved listings with optional filtering.

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Search by name/subtitle | `?q=museum` |
| `category` | string | Filter by category | `?category=Food & Restaurants` |
| `location` | string | Filter by city/country | `?location=London` |

**Example Request:**

```bash
curl "http://127.0.0.1:8000/api/listings/?q=museum&location=London"
```

**Example Response:**

```json
{
  "listings": [
    {
      "id": 1,
      "name": "British Museum",
      "subtitle": "World-class museum with accessible facilities",
      "lat": 51.5194,
      "lng": -0.1270,
      "rating": 4.8,
      "reviews_count": 42,
      "categories": ["Entertainment", "Culture"],
      "accessibility_features": ["wheelchair", "braille", "hearing_loop"],
      "status": "open",
      "city": "London",
      "country": "United Kingdom"
    }
  ]
}
```

---

## 🚢 Deployment Guide

### Deploy to Google Cloud Run

**Prerequisites:**
- Google Cloud account
- `gcloud` CLI installed

**Step 1: Build Docker Image**

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/accessadvisr .
```

**Step 2: Push to Google Container Registry**

```bash
docker push gcr.io/YOUR_PROJECT_ID/accessadvisr
```

**Step 3: Deploy to Cloud Run**

```bash
gcloud run deploy accessadvisr \
  --image gcr.io/YOUR_PROJECT_ID/accessadvisr \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "PRODUCTION=True,DJANGO_SECRET_KEY=your_secret_key" \
  --set-env-vars "GOOGLE_MAPS_BROWSER_KEY=your_key,GOOGLE_MAPS_SERVER_KEY=your_key"
```

**Step 4: Configure Database**

For production, use PostgreSQL:

```bash
# Set DATABASE_URL environment variable
gcloud run services update accessadvisr \
  --set-env-vars "DATABASE_URL=postgresql://user:pass@host/dbname"
```

**Step 5: Run Migrations**

```bash
# Connect to Cloud Run instance and run migrations
gcloud run services update accessadvisr --command "python,manage.py,migrate"
```

### Environment Variables for Production

```bash
PRODUCTION=True
DEBUG=False
DJANGO_SECRET_KEY=your_production_secret_key
GOOGLE_MAPS_BROWSER_KEY=your_browser_key
GOOGLE_MAPS_SERVER_KEY=your_server_key
DATABASE_URL=postgresql://user:pass@host/dbname
CUSTOM_DOMAIN=yourdomain.com
```

---

## ✅ Testing & Quality Assurance

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Manual Testing Checklist

- [ ] Homepage loads correctly
- [ ] Map displays with markers
- [ ] Search filters work
- [ ] Listing detail page shows all info
- [ ] Review submission works
- [ ] Admin dashboard accessible
- [ ] Moderation actions work
- [ ] Mobile responsive design
- [ ] Accessibility features (keyboard navigation, screen readers)

---

## 🐛 Common Issues & Solutions

### Issue 1: Map not showing

**Symptoms:** Blank map area, console errors

**Solutions:**
1. Check if `GOOGLE_MAPS_BROWSER_KEY` is set in `.env`
2. Verify billing is enabled in Google Cloud Console
3. Check if Maps JavaScript API is enabled
4. Inspect browser console for specific errors

### Issue 2: Geocoding fails

**Symptoms:** Listings have no lat/lng coordinates

**Solutions:**
1. Check if `GOOGLE_MAPS_SERVER_KEY` is set
2. Verify Geocoding API is enabled
3. Check API key restrictions (IP whitelist)
4. Ensure internet connection is active

### Issue 3: Static files not loading

**Symptoms:** No CSS/JS, broken styling

**Solutions:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings.py
# Ensure WhiteNoise is in MIDDLEWARE
```

### Issue 4: Database errors

**Symptoms:** "no such table" errors

**Solutions:**
```bash
# Run migrations
python manage.py migrate

# If issues persist, reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_london_venues
```

---

## 🎓 Best Practices

### 1. **Code Organization**

- Keep views focused (single responsibility)
- Use Django's built-in features (ORM, forms, admin)
- Separate business logic into utility functions
- Use template partials for reusable components

### 2. **Security**

- Never commit `.env` files
- Use environment variables for secrets
- Enable CSRF protection (Django default)
- Validate and sanitize user input
- Use Django's built-in authentication

### 3. **Performance**

- Use database indexes on frequently queried fields
- Implement pagination for large datasets
- Cache API responses
- Optimize images
- Use CDN for static files in production

### 4. **Accessibility**

- Use semantic HTML
- Add ARIA labels to interactive elements
- Ensure keyboard navigation works
- Test with screen readers
- Maintain color contrast ratios (WCAG AA)

### 5. **Git Workflow**

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request on GitHub
```

---

## 📚 Additional Resources

### Django Documentation
- [Official Django Docs](https://docs.djangoproject.com/)
- [Django ORM Tutorial](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)

### Google Maps Platform
- [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Geocoding API](https://developers.google.com/maps/documentation/geocoding)
- [Places API](https://developers.google.com/maps/documentation/places/web-service)

### Deployment
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 💬 Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Review Django/Google Maps documentation

---

**Built with ❤️ for accessibility**
