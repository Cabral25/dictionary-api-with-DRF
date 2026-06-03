from .views import *
from django.urls import path, include


urlpatterns = [
    path('', HomeView.as_view()),
    path('users/', include('dictionary_api.users.urls')),
    path('v1/', include('dictionary_api.v1.urls')),
    path('v2/', include('dictionary_api.v2.urls')),
    path('v3/', include('dictionary_api.v3.urls')),
]