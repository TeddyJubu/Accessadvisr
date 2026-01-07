#!/bin/sh

# exit on error
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding London venues..."
# This command is designed to be idempotent and won't duplicate data if it exists
python manage.py seed_london_venues

echo "Note: London venues already have coordinates, no geocoding needed."

echo "Starting Gunicorn..."
exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 60 accessadvisr.wsgi:application
