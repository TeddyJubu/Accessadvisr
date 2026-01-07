#!/bin/sh

# exit on error
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding default data for demo..."
# This command is designed to be idempotent and won't duplicate data if it exists
python manage.py seed_listings

echo "Geocoding listings for map visibility..."
python manage.py geocode_listings

echo "Starting Gunicorn..."
exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 60 accessadvisr.wsgi:application
