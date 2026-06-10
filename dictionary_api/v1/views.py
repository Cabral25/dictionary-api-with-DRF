from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from ..models import Word
from .serializers import WordSerializerV1, LoginSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework import status


class ListWords(ListCreateAPIView):
    """
        Endpoint que permite listar as palavras
        registradas e registrar novas. Usa a versão 
        1 do serializador de palavras. Qualquer um 
        pode acessar essa rota, mas somente admins 
        podem criar objetos.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializerV1

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]



class DetailWordView(RetrieveAPIView):
    """
        Rota que permite mostrar em detalhes uma
        palavra registrada. Usa a versão 1 do
        serializador de palavras. Qualquer um pode
        acessar essa rota.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializerV1
    permission_classes = [AllowAny]
    lookup_field = 'word'



class SearchWordView():
    pass



class UpdateWordView():
    pass



class DeleteWordView():
    pass



class LoginView(APIView):
    
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
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {
                'message': 'Logout realizado com sucesso'
            },
            status=status.HTTP_200_OK
        )