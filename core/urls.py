# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings_list, name='listings_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('api/listings/', views.listings_api, name='listings_api'),
]
