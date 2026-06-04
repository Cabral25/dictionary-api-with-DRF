from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from ..models import Word
from .serializers import WordSerializerV1

from django.contrib.auth import authenticate, login
from rest_framework import status


class ListWords(ListCreateAPIView):
    """
        Endpoint que permite listar as palavras
        registradas. Usa a versão 1 do serializador
        de palavras. Qualquer um pode acessar essa
        rota, mas somente admins podem criar objetos.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializerV1

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


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