# accessadvisr/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dj-admin/', admin.site.urls),  # Django's built-in admin
    path('', include('core.urls')),
]
