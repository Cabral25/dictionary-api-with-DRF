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
    
    def validate_word(self, value):

        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                'A palavra não pode conter números.'
            )
        return value

    def validate_meaning(self, value):
        
        if value.isdigit():
            raise serializers.ValidationError(
                'O significado não pode conter apenas números.'
            )
        
        return value


class LoginSerializer(Serializer):
    """"
        Serializador do login.
    """
    username = serializers.CharField()
    password = serializers.CharField()