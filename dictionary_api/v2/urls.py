from .views import *
from django.urls import path

urlpatterns = [
    path('words/', ListWordsv2.as_view(), name='words-v2'),
    path('words/search/', SearchWordViewV2.as_view(), name='search-word-v2'),
    path('words/<str:word>/', DetailWordViewV2.as_view(), name='word-detail-v2'),
    path('words/update/<str:word>/', UpdateWordViewV2.as_view(), name='update-word-v2'),
    path('words/delete/<str:word>/', DeleteWordViewV2.as_view(), name='delete-word-v2'),
    path('login/', LoginViewV2.as_view(), name='login-v2'),
    path('logout/', LogoutViewV2.as_view(), name='logout-v2')
]