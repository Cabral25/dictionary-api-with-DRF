from .views import *
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', ListWords.as_view()),
    path('login/', obtain_auth_token, name='login-v2'),
]