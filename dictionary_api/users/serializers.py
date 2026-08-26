from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

# from ..models import User


User = get_user_model()


class UserSerializer(ModelSerializer):
    """
        Serializer responsável pela serialização e
        desserialização de usuários da aplicação.

        Funções principais:
        - converter objetos User em JSON;
        - validar dados recebidos da API;
        - criar usuários no banco de dados;
        - controlar quais campos serão expostos.

        Campos expostos:
        - id
        - username
        - password
        - email
        - is_staff
        - is_superuser
        - is_active

        O campo password é definido como write_only,
        permitindo que a senha seja enviada no cadastro,
        mas impedindo que ela seja retornada nas respostas
        da API por questões de segurança.
    """
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


    def validate_username(self, value):
        return value


    def validate_password(self, value):
        return value