from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ..models import Word

from .serializers import WordSerializerV2

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView
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
    authentication_classes = []


class DetailWordViewV2(BaseDetailWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



class SearchWordViewV2(BaseSearchWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



class UpdateWordViewV2(BaseUpdateWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



class DeleteWordViewV2(BaseDeleteWordView):
    serializer_class = WordSerializerV2
    authentication_classes = []



class LoginViewV2():
    pass