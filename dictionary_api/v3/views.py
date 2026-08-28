from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import WordSerializerV3

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView,
    BaseLoginView,
    BaseAPIViewV3
)


"""
    A versão 3 dessa API utiliza o JWTauthentication como
    método de autenticação.
"""


class ListWordsV3(BaseAPIViewV3, BaseListWords):
    """
        Endpoint que permite listar as palavras
        registradas e registrar novas. Usa a versão 
        3 do serializador de palavras. Qualquer um 
        pode acessar essa rota, mas somente admins 
        podem criar objetos.
    """
    pass



class DetailWordViewV3(BaseDetailWordView):
    """
        Rota que permite mostrar em detalhes uma
        palavra registrada. Usa a versão 3 do
        serializador de palavras. Qualquer um pode
        acessar essa rota.
    """
    serializer_class = WordSerializerV3



class SearchWordViewV3(BaseSearchWordView):
    """
        View que permite buscar uma palavra.
        Qualquer um tem acesso.
    """
    serializer_class = WordSerializerV3



class UpdateWordViewV3(BaseAPIViewV3, BaseUpdateWordView):
    """
        Permite visualizar e atualizar uma palavra.
        Apenas administradores podem acessar essa view.
    """
    pass



class DeleteWordViewV3(BaseAPIViewV3, BaseDeleteWordView):
    """
        Permite apagar uma palavra.
        Apenas administradores podem apagar palavras.
    """
    pass


class LoginViewV3(BaseLoginView):
    """
        Permite ao usuário fazer login.
    """
    
    def post(self, request):

        user = self.authenticate_user(request)

        refresh = RefreshToken.for_user(user=user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        )


class LogoutViewV3(APIView):
    """
        Permite ao usuário fazer logout.
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {
                    'error': 'O refresh token é obrigatório.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {
                    'message': 'Logout realizado com sucesso.'
                },
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {
                    'error': 'Refresh token inválido.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class RefreshView(APIView):
    """
        View responsável por gerar um novo access token a partir de um refresh token válido.
        O cliente deve enviar o refresh token no corpo da requisição.
        Caso o token seja válido, um novo access token é retornado.
        Caso contrário, a API retorna uma mensagem de erro.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.data.get('refresh')

        if not refresh:
            return Response(
                {
                    'error': 'O refresh token é obrigatório.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh)
            return Response(
                {
                    'access': str(token.access_token)
                }
            )
        except TokenError:
            return Response(
                {
                    'error': 'Refresh token inválido.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )