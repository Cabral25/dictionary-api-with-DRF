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


class ListWordsV3(BaseAPIViewV3, BaseListWords):
    pass



class DetailWordViewV3(BaseDetailWordView):
    serializer_class = WordSerializerV3



class SearchWordViewV3(BaseSearchWordView):
    serializer_class = WordSerializerV3



class UpdateWordViewV3(BaseAPIViewV3, BaseUpdateWordView):
    pass



class DeleteWordViewV3(BaseAPIViewV3, BaseDeleteWordView):
    pass


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


class LogoutViewV3(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {
                    'message': 'Logout realizado com sucesso.'
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {
                    'error': 'Refresh token inválido.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class RefreshView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.data.get('refresh')

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