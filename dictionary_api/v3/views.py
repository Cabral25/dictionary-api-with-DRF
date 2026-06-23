from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Word

from .serializers import WordSerializerV3

from ..views import (
    BaseListWords,
    BaseDetailWordView,
    BaseSearchWordView,
    BaseUpdateWordView,
    BaseDeleteWordView,
    BaseLoginView
)


class ListWordsV3(BaseListWords):
    serializer_class = WordSerializerV3
    authentication_classes = [JWTAuthentication]



class DetailWordViewV3(BaseDetailWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class SearchWordViewV3(BaseSearchWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class UpdateWordViewV3(BaseUpdateWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []



class DeleteWordViewV3(BaseDeleteWordView):
    serializer_class = WordSerializerV3
    authentication_classes = []


class LoginViewV3(BaseLoginView):
    
    def post(self, request):

        user = self.authenticate_user(request)

        refresh = RefreshToken.for_user(user=user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        )