from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from ..models import Word

from .serializers import WordSerializerV2

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView,
    BaseLoginView
)


class ListWordsv2(BaseListWords):
    """
        Endpoint que permite listar as palavras
        registradas e registrar novas. Usa a versão 
        2 do serializador de palavras. Qualquer um 
        pode acessar essa rota, mas somente admins 
        podem criar objetos.
    """
    serializer_class = WordSerializerV2
    authentication_classes = [TokenAuthentication]


class DetailWordViewV2(BaseDetailWordView):
    """
        Rota que permite mostrar em detalhes uma
        palavra registrada. Usa a versão 2 do
        serializador de palavras. Qualquer um pode
        acessar essa rota.
    """
    serializer_class = WordSerializerV2
    authentication_classes = []



class SearchWordViewV2(BaseSearchWordView):
    """"
        View que permite buscar uma palavra.
        Qualquer um tem acesso.
    """
    serializer_class = WordSerializerV2
    authentication_classes = []



class UpdateWordViewV2(BaseUpdateWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



class DeleteWordViewV2(BaseDeleteWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



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
    pass