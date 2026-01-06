# core/models.py
from django.db import models

class Listing(models.Model):
    name = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    categories = models.JSONField(default=list)  # ["Food & Restaurants", "Sport"]
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)  # optional full address
    phone = models.CharField(max_length=40, blank=True)
    price_min = models.IntegerField(null=True, blank=True)
    price_max = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(default=0)
    status = models.CharField(max_length=20, default="open")  # open|closed
    tags = models.JSONField(default=list)
    featured = models.BooleanField(default=False)
    reviews_count = models.IntegerField(default=0)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def location_text(self):
        return f"{self.city}, {self.country}"

    def __str__(self):
        return self.name
