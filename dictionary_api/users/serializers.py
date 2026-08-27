from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import re

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
        if len(value) < 8:
            raise serializers.ValidationError('O username deve possuir pelo menos 8 caracteres.')
        return value


    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('A senha deve possuir pelo menos 8 caracteres.')
        return value


    def validate_email(self, value):
        padrao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9._]+\.[A-Z|a-z]{2,}\b'
        resultado = re.search(padrao, value)
        if not resultado:
            raise serializers.ValidationError('Email inválido.')
        return value

def validate_email(value):
    padrao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9._]+\.[A-Z|a-z]{2,}\b'
    resultado = re.search(padrao, value)
    if not resultado:
        print('email inválido')
    print('email válido')

print(validate_email('ade@gmail.com'))