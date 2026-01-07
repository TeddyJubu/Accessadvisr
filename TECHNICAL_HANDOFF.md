# AccessAdvisr - Production Deployment Handoff

## 🚀 Deployment Overview
- **Production URL**: [https://accessadvisr-932375520212.us-central1.run.app](https://accessadvisr-932375520212.us-central1.run.app)
- **Frontend Assets**: Served via WhiteNoise / Firebase
- **Backend**: Python Django 5.x on Google Cloud Run
- **Database**: Cloud SQL (PostgreSQL via Firebase Data Connect)
- **Maps**: Google Maps Platform (Javascript API + Geocoding API)

## 🔑 Credentials & Secrets
All secrets are managed via Cloud Run Environment Variables:
- `DJANGO_SECRET_KEY`: `******` (Set in Cloud Run)
- `GOOGLE_MAPS_BROWSER_KEY`: `AIzaSyDH...` (Public, restricted by HTTP Referrer)
- `GOOGLE_MAPS_SERVER_KEY`: `AIzaSyBj...` (Private, restricted by IP)
- `DATABASE_URL`: Automatically managed by platform

## 🗺️ Google Maps Configuration
To ensure the map loads correctly, the **Browser API Key** must have the following HTTP Referrer restrictions in Google Cloud Console:
1. `https://accessadvisr-932375520212.us-central1.run.app/*`
2. `https://accessadvisr-932375520212.us-central1.run.app/`
3. `http://127.0.0.1:8000/*` (For local development)
4. `http://localhost:8000/*` (For local development)

## 🔄 Maintenance & Updates
To deploy a new version of the application:

1. **Install Google Cloud CLI** (if not installed):
   ```bash
   brew install --cask google-cloud-sdk
   ```

2. **Authenticate**:
   ```bash
   gcloud auth login
   gcloud config set project accessadvisr-prod-9a7b1
   ```

3. **Deploy Command**:
   ```bash
   gcloud run deploy accessadvisr \
     --source . \
     --region us-central1 \
     --allow-unauthenticated \
     --update-env-vars DJANGO_SECRET_KEY=access-advisr-prod-secret-9a7b1,PRODUCTION=True,DEBUG=False,GOOGLE_MAPS_BROWSER_KEY=AIzaSyDHcj7wVmd4QzftOAniu-BWQbmPpUBHDs4,GOOGLE_MAPS_SERVER_KEY=AIzaSyBjsGX8c9Ic-QQoaA5jzdhv-r9j6QOHsUY
   ```

## 🛠️ Troubleshooting
- **Map says "Oops! Something went wrong"**: Check the browser console. If `RefererNotAllowedMapError`, update API key restrictions.
- **Server Error (500)**: Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision" --limit 20`
- **Database Migrations**: The container automatically runs `python manage.py migrate` on startup.

## 📊 Admin Access
- **URL**: `/admin-page/` (Custom Dashboard) or `/dj-admin/` (Django Admin)
- **Superuser**: Create via `gcloud run jobs execute create-superuser ...` (or use local shell)
