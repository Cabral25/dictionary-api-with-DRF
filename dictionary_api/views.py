from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Word
from .serializers import WordSerializer


class HomeView(APIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


# Create your views here.
