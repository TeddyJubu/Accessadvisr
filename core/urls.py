# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings_list, name='listings_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/review/', views.submit_review, name='submit_review'),
    path('listing/<int:pk>/review/success/', views.review_success, name='review_success'),
    path('listing/<int:pk>/photos/upload/', views.upload_photos, name='upload_photos'),
    path('listing/<int:pk>/photos/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('listing/<int:pk>/photos/<int:photo_id>/set-primary/', views.set_primary_photo, name='set_primary_photo'),
    path('submit-listing/', views.submit_listing, name='submit_listing'),
    path('submit-listing/success/', views.listing_submission_success, name='listing_submission_success'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('admin-page/moderate/', views.admin_moderate, name='admin_moderate'),
    path('api/listings/', views.listings_api, name='listings_api'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
