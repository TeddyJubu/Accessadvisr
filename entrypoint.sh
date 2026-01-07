#!/bin/sh

# exit on error
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding London venues..."
python manage.py seed_london_venues

echo "Seeding sponsorship and donation data..."
python manage.py seed_sponsorship_donations

echo "Seeding blog posts..."
python manage.py seed_blog

echo "Seeding partners..."
python manage.py seed_partners

echo "Seeding about us data..."
python manage.py seed_about_us

echo "Data seeding complete!"

echo "Starting Gunicorn..."
exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 60 accessadvisr.wsgi:application
