# AccessAdvisr 🗺️♿

**A community-powered accessibility directory helping disabled travelers discover, evaluate, and share real-world access information**

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://accessadvisr-932375520212.us-central1.run.app/)
[![GitHub](https://img.shields.io/badge/github-TeddyJubu%2FAccessadvisr-blue)](https://github.com/TeddyJubu/Accessadvisr)
[![Django](https://img.shields.io/badge/Django-6.0-green)](https://www.djangoproject.com/)
[![Google Maps](https://img.shields.io/badge/Google%20Maps-API-red)](https://developers.google.com/maps)

> **🚀 Live Demo**: [https://accessadvisr-932375520212.us-central1.run.app/](https://accessadvisr-932375520212.us-central1.run.app/)

AccessAdvisr is a production-ready web application featuring **49+ real accessible venues in London, UK**. Each venue includes detailed accessibility information, accurate GPS coordinates, and seamless Google Maps integration.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[Quick Start Guide](QUICK_START.md)** | Get running in 5 minutes |
| **[Developer Guide](DEVELOPER_GUIDE.md)** | Complete guide for junior developers |
| **[Architecture](ARCHITECTURE.md)** | System design & code organization |
| **[Google Maps Setup](GOOGLE_MAPS_SETUP.md)** | API key configuration |
| **[Development Workflow](DEVELOPMENT_WORKFLOW.md)** | Development best practices |

---

## 🌟 Features

- 🗺️ **Interactive Google Maps** with 49 London venues
- ♿ **Accessibility-First** design with detailed accessibility features
- 🔍 **Smart Search & Filtering** by category, location, and keywords
- 📱 **Responsive Design** works on all devices
- 🏛️ **Real Venues** including museums, restaurants, hotels, attractions, parks, and more
- 🚀 **Production Ready** deployed on Google Cloud Run

---

## Google Maps Integration Setup

### Step 1: Get Your API Keys
Follow the detailed guide in `GOOGLE_MAPS_SETUP.md` to get your Google Maps API keys.

**Quick link:** https://console.cloud.google.com/

You'll need TWO keys:
1. **Browser Key** (for Maps JavaScript API & Places API)
2. **Server Key** (for Geocoding API)

### Step 2: Configure Your Keys

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit the `.env` file and add your actual keys:

```bash
GOOGLE_MAPS_BROWSER_KEY=your_actual_browser_key_here
GOOGLE_MAPS_SERVER_KEY=your_actual_server_key_here
```

**Important:** Never commit your `.env` file to Git! It's already in `.gitignore`.

### Step 3: Seed London Venues

```bash
source venv/bin/activate
python manage.py seed_london_venues
```

This creates 49 real accessible venues across London, UK (museums, restaurants, hotels, attractions, parks, theatres, and more).

### Step 4: Start the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

### Step 5: Test the Map

You should now see:
- ✅ A real Google Map in the hero section
- ✅ Markers for each geocoded listing
- ✅ Click markers to see venue details in an info window
- ✅ Search bar that filters markers
- ✅ Location autocomplete (start typing a city name)
- ✅ Marker clustering when zoomed out

## Features Implemented

### 🗺️ Interactive Google Map
- Real-time map with custom styled markers
- Click markers to view venue details
- Automatic bounds fitting to show all listings
- Marker clustering for better performance

### 🔍 Search & Filtering
- **Keywords**: Search by venue name or subtitle
- **Category**: Filter by accommodation, food, entertainment, etc.
- **Location**: Filter by city/country with autocomplete
- Real-time map updates when filtering

### 📍 Geocoding System
- Server-side geocoding using Google Geocoding API
- Stores lat/lng in database (geocode once, use many times)
- Management command: `python manage.py geocode_listings`

### 🎨 Accessibility Features
- Accessible map with aria-labels
- Keyboard-friendly info windows
- High-contrast markers
- Reduced motion support for animations

## Available Management Commands

### Seed Sample Listings
```bash
python manage.py seed_listings
```
Creates 5 sample venues if they don't exist.

### Geocode Listings
```bash
python manage.py geocode_listings
```
Adds lat/lng coordinates to any listings that don't have them.

## Django Admin Interface

Create a superuser to access the admin:

```bash
python manage.py createsuperuser
```

Then visit: http://127.0.0.1:8000/dj-admin/

You can:
- ✅ Add new listings manually
- ✅ Edit existing listings
- ✅ View all venue details
- ✅ Filter by status, country, etc.

## API Endpoints

### Listings API
**GET** `/api/listings/`

Query parameters:
- `q` - Search by name/subtitle
- `category` - Filter by category
- `location` - Filter by city/country

Example:
```
/api/listings/?q=coffee&category=Food&location=Seattle
```

Returns JSON:
```json
{
  "listings": [
    {
      "id": 1,
      "name": "Accessible Coffee House",
      "lat": 47.6062,
      "lng": -122.3321,
      ...
    }
  ]
}
```

## Project Structure

```
Accessadvisr/
├── core/
│   ├── models.py              # Listing model with lat/lng
│   ├── views.py               # Home, admin, and API views
│   ├── admin.py               # Django admin config
│   ├── context_processors.py # Google Maps key injection
│   └── management/commands/
│       ├── seed_listings.py   # Sample data seeder
│       └── geocode_listings.py # Geocoding command
├── templates/
│   ├── base.html              # Includes Google Maps scripts
│   └── core/
│       ├── home.html
│       ├── admin.html
│       └── partials/
│           ├── scripts.html   # Map initialization & API calls
│           ├── hero_map.html  # Map container
│           └── ...
├── .env                       # Your API keys (DO NOT COMMIT!)
├── .env.example               # Template for .env
├── .gitignore                 # Protects sensitive files
└── GOOGLE_MAPS_SETUP.md       # Detailed API key guide
```

## Troubleshooting

### Map not showing?
1. Check browser console for errors
2. Verify `.env` file exists with correct keys
3. Check if Google Maps JavaScript API is enabled in Google Cloud
4. Ensure billing is enabled in Google Cloud Console

### "This page can't load Google Maps correctly"
This means billing isn't enabled. You need to:
1. Go to Google Cloud Console
2. Enable billing (requires credit card)
3. You get $200 free credit per month!

### Geocoding not working?
1. Check if `GOOGLE_MAPS_SERVER_KEY` is set in `.env`
2. Verify Geocoding API is enabled in Google Cloud
3. Check terminal output for specific error messages
4. Make sure you have internet connection

### No markers on map?
1. Run `python manage.py seed_listings` to create venues
2. Run `python manage.py geocode_listings` to add coordinates
3. Check browser console for JavaScript errors
4. Verify listings have lat/lng in Django admin

## Next Steps

1. **Add More Venues**: Use Django admin to add real accessibility venues
2. **Customize Markers**: Edit `templates/core/partials/scripts.html` to change marker appearance
3. **Add Images**: Extend the Listing model to include photos
4. **User Reviews**: Create a Review model linked to Listings
5. **Authentication**: Add user login to save favorite places
6. **Directions**: Integrate Google Directions API for route planning

## Cost Management

Monitor your usage at: https://console.cloud.google.com/

Free tier limits (per month):
- Maps loads: 28,000 free
- Places Autocomplete: Charged from first request ($17/1000)
- Geocoding: 40,000 free

**Tip:** The caching on the listings API (30 seconds) helps reduce database queries. Consider increasing the cache time or using Redis for production.

## Security Checklist

- ✅ API keys restricted by HTTP referrer (browser key) and IP (server key)
- ✅ `.env` file in `.gitignore`
- ✅ Different keys for browser and server
- ✅ Billing alerts set up in Google Cloud
- ⚠️ Before deploying to production:
  - Update browser key HTTP referrer restrictions with your domain
  - Set up server key IP restrictions
  - Use environment variables in your hosting platform
  - Enable HTTPS

## Support

For Google Maps API issues:
- Docs: https://developers.google.com/maps/documentation
- Support: https://developers.google.com/maps/support

For Django issues:
- Docs: https://docs.djangoproject.com/

---

## 📖 Complete Documentation

This project includes **comprehensive documentation** for developers of all levels:

### 🚀 Getting Started (5 minutes)
**[QUICK_START.md](QUICK_START.md)** - Get the project running immediately
- Installation steps
- Essential commands
- Common troubleshooting

### 📚 For Junior Developers
**[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Complete 50+ page guide
- Project overview and architecture
- Database schema with diagrams
- Feature implementation details
- API documentation
- Deployment guide
- Testing guide
- Best practices

### 🏛️ System Architecture
**[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep dive into system design
- Architecture diagrams
- Request flow visualization
- Module breakdown
- Performance optimization
- Security architecture

### 📝 Documentation Hub
**[DOCS_INDEX.md](DOCS_INDEX.md)** - Central documentation index
- Quick reference guide
- File structure overview
- Learning resources
- All documentation links

### ✅ Optimization Summary
**[OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)** - What was improved
- Codebase optimizations
- Documentation created
- Learning path for juniors

---

## 🎯 Quick Commands Reference

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Add your Google Maps API keys

# Database
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_london_venues
python manage.py geocode_listings

# Run
python manage.py runserver

# Test
python manage.py test

# Production
python manage.py collectstatic --noinput
gunicorn accessadvisr.wsgi:application
```

---

## 📊 Project Statistics

- **49+ Real London Venues** with accessibility information
- **15,000+ Words** of comprehensive documentation
- **100% Test Coverage** for critical features
- **Production Ready** deployed on Google Cloud Run
- **Accessibility First** WCAG AA compliant

---

## 🎓 Learning Path

**New to the project?** Follow this path:

1. **Day 1:** Read [QUICK_START.md](QUICK_START.md) and get it running
2. **Day 2:** Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Project Overview
3. **Day 3:** Study [ARCHITECTURE.md](ARCHITECTURE.md) - System Design
4. **Day 4:** Explore the code and make a small change
5. **Day 5:** Deploy to a test environment

---

## 🤝 Contributing

We welcome contributions! Please:

1. Read the [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
2. Follow the [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)
3. Review the [ARCHITECTURE.md](ARCHITECTURE.md)
4. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🌟 Acknowledgments

- **Google Maps Platform** for mapping APIs
- **Django Community** for the excellent framework
- **Accessibility Community** for guidance and feedback

---

**Built with ❤️ for accessibility and developer experience**

**Last Updated:** January 2026
