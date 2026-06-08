from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from ..models import Word


class WordSerializerV1(ModelSerializer):
    """
        Serializer responsável pela serialização e
        desserialização de palavras registradas.

        Funções principais:
        - converter objetos Word em JSON;
        - validar dados recebidos da API;
        - criar palavras no banco de dados;
        - controlar quais campos serão expostos.
    """
    
    class Meta:
        model = Word
        fields = ['word', 'meaning']
        read_only_fields = [
            'created_by',
            'created_at',
            'updated_at'
        ]


class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()