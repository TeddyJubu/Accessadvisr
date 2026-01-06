# Google Maps API Keys Setup Guide

This guide will walk you through getting your Google Maps API keys from the Google Cloud Console.

## Prerequisites
- A Google account
- A credit card (required for Google Cloud, but you get $200 free credit monthly)

## Step-by-Step Instructions

### 1. Access Google Cloud Console
1. Go to: https://console.cloud.google.com/
2. Sign in with your Google account

### 2. Create a New Project
1. Click the project dropdown at the top of the page
2. Click "NEW PROJECT"
3. Enter project name: `AccessAdvisr` (or any name you prefer)
4. Click "CREATE"
5. Wait for the project to be created, then select it from the dropdown

### 3. Enable Required APIs
You need to enable these APIs:
1. In the left sidebar, go to "APIs & Services" > "Library"
2. Search for and enable each of these:
   - **Maps JavaScript API** (for browser map display)
   - **Places API** (for location autocomplete)
   - **Geocoding API** (for server-side address→coordinates conversion)

For each API:
- Click on the API name
- Click the blue "ENABLE" button
- Wait for it to enable

### 4. Create API Keys

#### Create Browser Key (Maps JavaScript API)
1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "API key"
4. A popup will show your API key - **COPY IT** to a safe place
5. Click "RESTRICT KEY" (very important for security)
6. Give it a name: `AccessAdvisr Browser Key`
7. Under "Application restrictions":
   - Select "HTTP referrers (web sites)"
   - Click "ADD AN ITEM"
   - Add: `http://127.0.0.1:8000/*` (for local development)
   - Add: `http://localhost:8000/*` (alternative)
   - Later, add your production domain: `https://yourdomain.com/*`
8. Under "API restrictions":
   - Select "Restrict key"
   - Check:
     - Maps JavaScript API
     - Places API
9. Click "SAVE"

#### Create Server Key (Geocoding API)
1. Click "+ CREATE CREDENTIALS" again
2. Select "API key"
3. Copy the new API key to a safe place
4. Click "RESTRICT KEY"
5. Give it a name: `AccessAdvisr Server Key`
6. Under "Application restrictions":
   - Select "IP addresses"
   - Click "ADD AN ITEM"
   - For local development, you can leave this unrestricted OR
   - Add your server's IP address (for production)
7. Under "API restrictions":
   - Select "Restrict key"
   - Check:
     - Geocoding API
8. Click "SAVE"

### 5. Set Up Billing (Required but Free Tier Available)
1. Go to "Billing" in the left sidebar
2. Click "LINK A BILLING ACCOUNT"
3. Follow the prompts to add a credit card
4. **Note:** Google provides $200 free credit per month which is generous for small projects
5. You can set up budget alerts to avoid unexpected charges

### 6. Add Keys to Your Project

#### Method 1: Environment Variables (Recommended for production)
Create a `.env` file in your project root:

```bash
# .env
GOOGLE_MAPS_BROWSER_KEY=your_browser_key_here
GOOGLE_MAPS_SERVER_KEY=your_server_key_here
```

Then install python-dotenv:
```bash
source venv/bin/activate
pip install python-dotenv
```

Update `accessadvisr/settings.py` to load from .env:
```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Google Maps API Keys
GOOGLE_MAPS_BROWSER_KEY = os.getenv("GOOGLE_MAPS_BROWSER_KEY", "")
GOOGLE_MAPS_SERVER_KEY = os.getenv("GOOGLE_MAPS_SERVER_KEY", "")
```

#### Method 2: Export in Terminal (Quick for testing)
```bash
export GOOGLE_MAPS_BROWSER_KEY="your_browser_key_here"
export GOOGLE_MAPS_SERVER_KEY="your_server_key_here"
source venv/bin/activate
python manage.py runserver
```

**Important:** Never commit API keys to version control! Add `.env` to your `.gitignore` file.

### 7. Verify API Keys Work
Once you've set the keys, run:

```bash
source venv/bin/activate
# Seed some sample data
python manage.py seed_listings
# Geocode the listings (this tests your server key)
python manage.py geocode_listings
# Start the server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and you should see a real Google Map with markers!

## Cost Estimates
- **Maps JavaScript API**: 28,000 loads free per month, then $7 per 1,000 loads
- **Places API**: $17 per 1,000 requests (Autocomplete)
- **Geocoding API**: 40,000 requests free per month, then $5 per 1,000

For a small project, the free tier is usually sufficient!

## Security Best Practices
1. ✅ Always restrict API keys (we did this above)
2. ✅ Use different keys for browser and server
3. ✅ Never commit keys to Git
4. ✅ Set up billing alerts in Google Cloud Console
5. ✅ Monitor usage in the Google Cloud Console

## Troubleshooting

### "This page can't load Google Maps correctly"
- Check if billing is enabled in Google Cloud Console
- Verify the API key is correct in your .env file
- Check if Maps JavaScript API is enabled
- Check browser console for specific error messages

### "REQUEST_DENIED" error
- The API you're trying to use isn't enabled
- Go to Google Cloud Console > APIs & Services > Library
- Enable the required API

### Geocoding not working
- Check if GOOGLE_MAPS_SERVER_KEY is set correctly
- Verify Geocoding API is enabled
- Check the terminal output for specific error messages

## Next Steps
After setting up your keys:
1. Visit the instructions below for seeding data and testing the map
2. Customize marker styles and info windows
3. Add more listings through the Django admin
4. Deploy to production (remember to update HTTP referrer restrictions!)
