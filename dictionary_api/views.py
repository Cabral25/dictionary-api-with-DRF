from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication

from .models import Word

from .serializers import LoginSerializer
from dictionary_api.v2.serializers import WordSerializerV2
from dictionary_api.v3.serializers import WordSerializerV3

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import authenticate


class BaseListWords(ListCreateAPIView):
    """
        Classe base que serve para listar e
        criar palavras.
    """
    queryset = Word.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BaseAPIViewV2(GenericAPIView):
    serializer_class = WordSerializerV2
    authentication_classes = [TokenAuthentication]


class BaseAPIViewV3(GenericAPIView):
    serializer_class = WordSerializerV3
    authentication_classes = [JWTAuthentication]
    

class BaseDetailWordView(RetrieveAPIView):
    queryset = Word.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'word'


class BaseSearchWordView(ListAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):

        query = self.request.query_params.get('q')

        if not query:
            return Word.objects.none()
        
        # i = ignore case (encontra a palavra independente se ela estiver em maiúscula ou minúscula)
        # contains = contém
        # retorna a(s) palavra(s) que contém o valor de q em qualquer posição ({'q': 'casa'} retorna casa, casamento, etc)
        return Word.objects.filter(word__icontains=query)
    

class BaseUpdateWordView(RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    lookup_field = 'word'

    def get_permissions(self):
        
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [IsAdminUser()]


class BaseDeleteWordView(RetrieveUpdateDestroyAPIView):
    queryset = Word.objects.all()
    lookup_field = 'word'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]



class BaseLoginView(APIView):
    
    permission_classes = [AllowAny]

    def authenticate_user(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            raise AuthenticationFailed(
                'Credenciais inválidas'
            )
        
        return user


# Create your views here.
