from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .serializers import WordSerializerV1, LoginSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework import status

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView
)


class ListWords(BaseListWords):
    """
        Endpoint que permite listar as palavras
        registradas e registrar novas. Usa a versão 
        1 do serializador de palavras. Qualquer um 
        pode acessar essa rota, mas somente admins 
        podem criar objetos.
    """
    serializer_class = WordSerializerV1



class DetailWordView(BaseDetailWordView):
    """
        Rota que permite mostrar em detalhes uma
        palavra registrada. Usa a versão 1 do
        serializador de palavras. Qualquer um pode
        acessar essa rota.
    """
    serializer_class = WordSerializerV1



class SearchWordView(BaseSearchWordView):
    """"
        View que permite buscar uma palavra.
        Qualquer um tem acesso.
    """
    
    serializer_class = WordSerializerV1



class UpdateWordView(BaseUpdateWordView):
    """
        Permite visualizar e atualizar uma palavra.
        Apenas administradores podem acessar essa view.
    """
    serializer_class = WordSerializerV1



class DeleteWordView(BaseDeleteWordView):
    """
        Permite apagar uma palavra.
        Apenas administradores podem apagar palavras.
    """
    serializer_class = WordSerializerV1



class LoginView(APIView):
    """
        View básica para um usuário fazer login.
        O acesso é livre para todos.
    """
    
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

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
    


class LogoutView(APIView):
    """
        View simples para realizar o logout.
        O usuário precisa estar autenticado
        e logado para acessar essa view.
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {
                'message': 'Logout realizado com sucesso'
            },
            status=status.HTTP_200_OK
        )