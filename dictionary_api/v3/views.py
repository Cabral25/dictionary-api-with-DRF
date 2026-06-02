from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ..models import Word

from django.contrib.auth import authenticate, login


class ListWords(ListCreateAPIView):
    query = Word.objects.all()



class LoginView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {
                    'error': 'Credenciais inválidas'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        login(request, user)

        return Response(
            {
                'message': 'Login realizado com sucesso'
            },
            status=status.HTTP_200_OK
        )