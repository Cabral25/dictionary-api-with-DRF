from .views import *
from django.urls import path


urlpatterns = [
    path('words/', ListWords.as_view(), name='words'),
    path('words/<str:word>/', DetailWordView.as_view(), name='word-detail-v1'),
    path('login/', LoginView.as_view(), name='login-v1'),
    path('logout/', LogoutView.as_view(), name='logout-v1'),
]