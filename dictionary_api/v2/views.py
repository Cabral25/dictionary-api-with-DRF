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
        Qualquer um tem acesso.
    """
    serializer_class = WordSerializerV2



class UpdateWordViewV2(BaseAPIViewV2, BaseUpdateWordView):
    pass



class DeleteWordViewV2(BaseAPIViewV2, BaseDeleteWordView):
    pass



class LoginViewV2(BaseLoginView):
    
    def post(self, request):

        user = self.authenticate_user(request)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key
            }
        )
    


class LogoutViewV2(APIView):
    
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