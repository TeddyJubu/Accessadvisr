# ⚡ Quick Start Guide

**Get AccessAdvisr running in 5 minutes!**

---

## 🎯 Prerequisites

- Python 3.10+
- pip
- Google Maps API keys ([Get them here](GOOGLE_MAPS_SETUP.md))

---

## 🚀 Installation

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/TeddyJubu/Accessadvisr.git
cd Accessadvisr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google Maps API keys
# GOOGLE_MAPS_BROWSER_KEY=your_key_here
# GOOGLE_MAPS_SERVER_KEY=your_key_here
```

### 3. Initialize Database

```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Seed 49 London venues
python manage.py seed_london_venues

# Add GPS coordinates
python manage.py geocode_listings
```

### 4. Run Server

```bash
python manage.py runserver
```

**Visit:** http://127.0.0.1:8000/

---

## 📋 Common Commands

### Development

```bash
# Run development server
python manage.py runserver

# Access Django admin
# Visit: http://127.0.0.1:8000/dj-admin/

# Run tests
python manage.py test

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Data Management

```bash
# Seed sample data (5 venues)
python manage.py seed_listings

# Seed London venues (49 real venues)
python manage.py seed_london_venues

# Geocode listings (add GPS coordinates)
python manage.py geocode_listings

# Clear database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_london_venues
python manage.py geocode_listings
```

### Production

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn accessadvisr.wsgi:application --bind 0.0.0.0:8000
```

---

## 🗂️ Project Structure

```
Accessadvisr/
├── core/                    # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── urls.py             # URL routing
│   └── management/commands/ # Custom commands
├── templates/              # HTML templates
│   ├── base.html          # Base layout
│   └── core/              # App templates
├── accessadvisr/          # Project settings
│   └── settings.py        # Configuration
├── .env                   # Environment variables (create this!)
└── manage.py              # Django CLI
```

---

## 🔑 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Homepage with map |
| `/listings/` | All venues |
| `/listing/<id>/` | Venue detail |
| `/submit-listing/` | Add new venue |
| `/admin-page/` | Admin dashboard |
| `/dj-admin/` | Django admin |
| `/api/listings/` | JSON API |

---

## 🐛 Troubleshooting

### Map not showing?

1. Check `.env` has `GOOGLE_MAPS_BROWSER_KEY`
2. Enable billing in Google Cloud Console
3. Enable Maps JavaScript API

### No venues on map?

```bash
python manage.py seed_london_venues
python manage.py geocode_listings
```

### Database errors?

```bash
python manage.py migrate
```

### Static files not loading?

```bash
python manage.py collectstatic --noinput
```

---

## 📚 Next Steps

1. **Read full guide:** [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
2. **Setup Google Maps:** [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md)
3. **Learn workflow:** [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)

---

## 🆘 Need Help?

- Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed explanations
- Review [Django Documentation](https://docs.djangoproject.com/)
- Check [Google Maps Platform Docs](https://developers.google.com/maps)

---

**Happy coding! 🚀**
