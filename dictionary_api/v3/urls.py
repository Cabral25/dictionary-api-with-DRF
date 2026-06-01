from .views import *
from django.urls import path, include

urlpatterns = [
    path('', ListWords.as_view()),
]