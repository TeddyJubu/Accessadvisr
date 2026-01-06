# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-page/', views.admin_page, name='admin_page'),
]
