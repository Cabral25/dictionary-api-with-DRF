from .views import *
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('words/', ListWordsV3.as_view(), name='list-words-v3'),
    path('words/search/', SearchWordViewV3.as_view(), name='search-word-v3'),
    path('words/<str:word>/', DetailWordViewV3.as_view(), name='word-detail-v3'),
    path('words/update/<str:word>/', UpdateWordViewV3.as_view(), name='update-word-v3'),
    path('words/delete/<str:word>/', DeleteWordViewV3.as_view(), name='delete-word-v3'),
    path('login/', TokenObtainPairView.as_view(), name='login-v3'),
    path('logout/', LogoutViewV3.as_view(), name='logout-v3'),
    path('refresh/', TokenRefreshView.as_view()),
]