from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include


urlpatterns = [
    path('', HomeView.as_view())
]