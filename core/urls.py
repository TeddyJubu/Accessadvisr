# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings_list, name='listings_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/review/', views.submit_review, name='submit_review'),
    path('listing/<int:pk>/review/success/', views.review_success, name='review_success'),
    path('submit-listing/', views.submit_listing, name='submit_listing'),
    path('submit-listing/success/', views.listing_submission_success, name='listing_submission_success'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('api/listings/', views.listings_api, name='listings_api'),
]
