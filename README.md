# AccessAdvisr - Quick Start Guide

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

### Step 3: Seed Sample Data

```bash
source venv/bin/activate
python manage.py seed_listings
```

This creates 5 sample accessibility venues across different US cities.

### Step 4: Geocode the Listings

```bash
python manage.py geocode_listings
```

This will use your Server API key to convert addresses to lat/lng coordinates.

### Step 5: Start the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

### Step 6: Test the Map

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
