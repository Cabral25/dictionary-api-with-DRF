from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ..models import Word

from serializers import WordSerializerV3

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView
)


class ListWordsV3(BaseListWords):
    serializer_class = WordSerializerV3
    authentication_classes = []



class DetailWordViewV2(BaseDetailWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class SearchWordViewV2(BaseSearchWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class UpdateWordViewV2(BaseUpdateWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class DeleteWordViewV2(BaseDeleteWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []