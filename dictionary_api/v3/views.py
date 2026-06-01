from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ..models import Word


class ListWords(ListCreateAPIView):
    query = Word.objects.all()