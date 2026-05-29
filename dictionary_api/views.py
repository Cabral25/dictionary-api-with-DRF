from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .models import Word
from .serializers import WordSerializer


class HomeView(ListCreateAPIView):
    queryset = Word.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WordSerializer


# Create your views here.
