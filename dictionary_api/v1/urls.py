from .views import *
from django.urls import path


urlpatterns = [
    path('words/', ListWords.as_view(), name='words'),
    path('login/', LoginView.as_view(), name='login-v1'),
]