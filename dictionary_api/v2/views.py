from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .serializers import WordSerializerV2

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView,
    BaseLoginView,
    BaseAPIViewV2
)


"""
    A versão 2 dessa API utiliza o Token Authentication como
    método de autenticação.
    Funciona assim:

        1. O usuário envia suas credenciais, como username
           e password.
        2. A API verifica se essas credenciais são válidas.
        3. Se forem válidas, a API fornece um token associado
           àquele usuário.
        4. O cliente deve enviar esse token em todas as requisições
           para endpoints protegidas, geralmente no header:

                Authorization: Token seu_token_aqui
        
        5. O DRF verifica se o token existe e identifica o usuário
           associado a ele, disponibilizando-o através do request.user.

    Diferentemente da autenticação por sessão, não é necessário
    manter um cookie de sessão. E, diferentemente da versão 3,
    esse token normalmente é um valor armazenado no banco de dados
    e associado diretamente ao usuário.
"""


class ListWordsv2(BaseAPIViewV2, BaseListWords):
    """
        Endpoint que permite listar as palavras
        registradas e registrar novas. Usa a versão 
        2 do serializador de palavras. Qualquer um 
        pode acessar essa rota, mas somente admins 
        podem criar objetos.
    """
    pass


class DetailWordViewV2(BaseDetailWordView):
    """
        Rota que permite mostrar em detalhes uma
        palavra registrada. Usa a versão 2 do
        serializador de palavras. Qualquer um pode
        acessar essa rota.
    """
    serializer_class = WordSerializerV2



class SearchWordViewV2(BaseSearchWordView):
    """"
        View que permite buscar uma palavra.
        Qualquer um tem acesso a essa rota.
    """
    serializer_class = WordSerializerV2



class UpdateWordViewV2(BaseAPIViewV2, BaseUpdateWordView):
    """
        Permite atualizar uma palavra.
    """
    pass



class DeleteWordViewV2(BaseAPIViewV2, BaseDeleteWordView):
    """
        Permite deletar uma palavra. 
    """
    pass



class LoginViewV2(BaseLoginView):
    """
        Permite ao usuário fazer login.
    """
    
    def post(self, request):

        user = self.authenticate_user(request)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key
            }
        )
    


class LogoutViewV2(APIView):
    """
        Permite ao usuário fazer logout.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        request.user.auth_token.delete()

        return Response(
            {
                'message': 'Logout realizado com sucesso'
            },
            status=status.HTTP_200_OK
        )