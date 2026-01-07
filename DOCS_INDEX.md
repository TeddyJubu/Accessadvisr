# 📝 Code Documentation Index

**Complete reference for all AccessAdvisr documentation**

---

## 🎯 For New Developers

Start here if you're new to the project:

1. **[Quick Start Guide](QUICK_START.md)** ⚡
   - Get the project running in 5 minutes
   - Essential commands
   - Common troubleshooting

2. **[Developer Guide](DEVELOPER_GUIDE.md)** 📖
   - Complete walkthrough of the entire project
   - Database schema explained
   - Feature implementation details
   - Best practices

3. **[Architecture](ARCHITECTURE.md)** 🏛️
   - System design overview
   - Request flow diagrams
   - Module breakdown
   - Performance optimization

---

## 🔧 Setup & Configuration

### Initial Setup

- **[Quick Start Guide](QUICK_START.md)** - Installation steps
- **[Google Maps Setup](GOOGLE_MAPS_SETUP.md)** - API key configuration
- **[.env.example](.env.example)** - Environment variables template

### Development Workflow

- **[Development Workflow](DEVELOPMENT_WORKFLOW.md)** - Git workflow, testing, deployment
- **[TECHNICAL_HANDOFF.md](TECHNICAL_HANDOFF.md)** - Technical handoff notes

---

## 📚 Feature Documentation

### Core Features

1. **Google Maps Integration**
   - See: [Developer Guide - Google Maps Integration](DEVELOPER_GUIDE.md#1-google-maps-integration)
   - Files: `templates/core/partials/hero_map.html`, `scripts.html`

2. **Search & Filtering**
   - See: [Developer Guide - Search & Filtering](DEVELOPER_GUIDE.md#2-search--filtering)
   - Files: `core/views.py::listings_list`, `templates/core/listings_list.html`

3. **Geocoding System**
   - See: [Developer Guide - Geocoding System](DEVELOPER_GUIDE.md#3-geocoding-system)
   - Files: `core/utils.py::geocode_listing`, `core/management/commands/geocode_listings.py`

4. **Review System**
   - See: [Developer Guide - Review System](DEVELOPER_GUIDE.md#4-review-system)
   - Files: `core/models.py::Review`, `core/views.py::submit_review`

5. **Admin Dashboard**
   - See: [Developer Guide - Admin Dashboard](DEVELOPER_GUIDE.md#5-admin-dashboard)
   - Files: `core/views.py::admin_page`, `templates/core/admin.html`

---

## 🗂️ Code Reference

### Models

```
core/models.py
├── Category        # Venue categories with marker styling
├── Listing         # Accessible venue with location & features
└── Review          # User review with accessibility ratings
```

**Documentation:**
- [Database Schema](DEVELOPER_GUIDE.md#database-schema)
- [Architecture - Database Design](ARCHITECTURE.md#database-design)

### Views

```
core/views.py
├── home()                    # Homepage
├── listings_list()           # Venue list with filters
├── listing_detail()          # Single venue detail
├── submit_review()           # Review submission
├── submit_listing()          # User-submitted venue
├── admin_page()              # Admin dashboard
├── admin_moderate()          # Moderation actions
└── listings_api()            # JSON API endpoint
```

**Documentation:**
- [Feature Implementation](DEVELOPER_GUIDE.md#feature-implementation)
- [Architecture - Module Breakdown](ARCHITECTURE.md#module-breakdown)

### Templates

```
templates/
├── base.html                 # Global layout
└── core/
    ├── home.html             # Homepage
    ├── listings_list.html    # Venue list
    ├── listing_detail.html   # Venue detail
    ├── submit_listing.html   # Add venue form
    ├── admin.html            # Admin dashboard
    └── partials/             # Reusable components
        ├── hero_map.html
        ├── search_bar.html
        ├── scripts.html      # JavaScript
        └── ...
```

**Documentation:**
- [Template Organization](ARCHITECTURE.md#template-organization)

### Management Commands

```
core/management/commands/
├── seed_listings.py          # Seed 5 sample venues
├── seed_london_venues.py     # Seed 49 London venues
├── geocode_listings.py       # Add GPS coordinates
└── fetch_london_data.py      # Fetch real venue data
```

**Usage:**
```bash
python manage.py seed_london_venues
python manage.py geocode_listings
```

**Documentation:**
- [Quick Start - Data Management](QUICK_START.md#data-management)

---

## 🚀 Deployment

### Production Deployment

- **[Developer Guide - Deployment](DEVELOPER_GUIDE.md#deployment-guide)**
- **[Architecture - Deployment Architecture](ARCHITECTURE.md#deployment-architecture)**

### Environment Configuration

```bash
# Development
DEBUG=True
PRODUCTION=False

# Production
DEBUG=False
PRODUCTION=True
DATABASE_URL=postgresql://...
```

**Documentation:**
- [.env.example](.env.example)
- [Developer Guide - Setup](DEVELOPER_GUIDE.md#setup-guide)

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

**Documentation:**
- [Developer Guide - Testing](DEVELOPER_GUIDE.md#testing--quality-assurance)
- [Architecture - Testing Architecture](ARCHITECTURE.md#testing-architecture)

---

## 🔍 API Reference

### Endpoints

```
GET  /api/listings/              # List all approved listings
     ?q=museum                   # Filter by keyword
     &category=Entertainment     # Filter by category
     &location=London            # Filter by location
```

**Documentation:**
- [Developer Guide - API Documentation](DEVELOPER_GUIDE.md#api-documentation)
- [Architecture - API Architecture](ARCHITECTURE.md#api-architecture)

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution | Documentation |
|-------|----------|---------------|
| Map not showing | Check API keys, enable billing | [Quick Start - Troubleshooting](QUICK_START.md#troubleshooting) |
| No venues on map | Run seed & geocode commands | [Developer Guide - Common Issues](DEVELOPER_GUIDE.md#common-issues--solutions) |
| Database errors | Run migrations | [Quick Start - Troubleshooting](QUICK_START.md#troubleshooting) |
| Static files not loading | Run collectstatic | [Developer Guide - Common Issues](DEVELOPER_GUIDE.md#issue-3-static-files-not-loading) |

---

## 📊 Project Statistics

### Codebase Overview

```
Language          Files    Lines    Code
─────────────────────────────────────────
Python               15    2,500   2,000
HTML                 20    3,500   3,000
JavaScript            1      500     400
CSS                   0        0       0 (using Tailwind CDN)
Markdown              8    5,000   4,500
─────────────────────────────────────────
Total                44   11,500  10,000
```

### Features

- ✅ 49+ real London venues
- ✅ Google Maps integration
- ✅ Search & filtering
- ✅ Review system with moderation
- ✅ Admin dashboard
- ✅ Responsive design
- ✅ Accessibility-first
- ✅ Production-ready

---

## 🎓 Learning Resources

### Django

- [Official Django Documentation](https://docs.djangoproject.com/)
- [Django ORM Tutorial](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [Django Forms Guide](https://docs.djangoproject.com/en/stable/topics/forms/)

### Google Maps Platform

- [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Geocoding API](https://developers.google.com/maps/documentation/geocoding)
- [Places API](https://developers.google.com/maps/documentation/places/web-service)

### Deployment

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

## 📁 File Structure Quick Reference

```
Accessadvisr/
├── 📂 accessadvisr/              # Django project config
│   ├── settings.py               # ⚙️ Configuration
│   ├── urls.py                   # 🔗 Root routing
│   └── wsgi.py                   # 🌐 WSGI entry
│
├── 📂 core/                      # Main application
│   ├── models.py                 # 🗄️ Database models
│   ├── views.py                  # 🎯 Business logic
│   ├── urls.py                   # 🔗 App routing
│   ├── forms.py                  # 📝 Forms
│   ├── utils.py                  # 🛠️ Utilities
│   ├── admin.py                  # 🔧 Django admin
│   └── management/commands/      # 🌱 Custom commands
│
├── 📂 templates/                 # HTML templates
│   ├── base.html                 # 🎨 Base layout
│   └── core/                     # App templates
│       ├── home.html
│       ├── listings_list.html
│       ├── listing_detail.html
│       └── partials/             # Reusable components
│
├── 📂 Documentation/
│   ├── README.md                 # 📖 Main readme
│   ├── QUICK_START.md            # ⚡ Quick start
│   ├── DEVELOPER_GUIDE.md        # 📚 Complete guide
│   ├── ARCHITECTURE.md           # 🏛️ Architecture
│   ├── GOOGLE_MAPS_SETUP.md      # 🗺️ Maps setup
│   ├── DEVELOPMENT_WORKFLOW.md   # 🔄 Workflow
│   └── DOCS_INDEX.md             # 📝 This file
│
├── .env                          # 🔐 Environment vars
├── .env.example                  # 📋 Env template
├── requirements.txt              # 📦 Dependencies
├── manage.py                     # 🎮 Django CLI
└── Dockerfile                    # 🐳 Container config
```

---

## 🔗 Quick Links

### Essential Files

- [settings.py](accessadvisr/settings.py) - Django configuration
- [models.py](core/models.py) - Database models
- [views.py](core/views.py) - Business logic
- [urls.py](core/urls.py) - URL routing
- [requirements.txt](requirements.txt) - Python dependencies

### Documentation

- [README.md](README.md) - Project overview
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Complete developer guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture documentation

### Configuration

- [.env.example](.env.example) - Environment variables template
- [Dockerfile](Dockerfile) - Docker configuration
- [.gitignore](.gitignore) - Git ignore rules

---

## 🤝 Contributing

1. Read the [Developer Guide](DEVELOPER_GUIDE.md)
2. Follow the [Development Workflow](DEVELOPMENT_WORKFLOW.md)
3. Review the [Architecture](ARCHITECTURE.md)
4. Submit a pull request

---

## 📞 Support

For questions or issues:
- Check the [Troubleshooting](QUICK_START.md#troubleshooting) section
- Review the [Common Issues](DEVELOPER_GUIDE.md#common-issues--solutions)
- Open an issue on GitHub

---

**Last Updated:** January 2026

**Built with ❤️ for accessibility**
