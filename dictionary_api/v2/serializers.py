from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Word


class WordSerializerV2(ModelSerializer):
    """
        Serializer responsável pela serialização e
        desserialização de palavras registradas.

        Funções principais:
        - converter objetos Word em JSON;
        - validar dados recebidos da API;
        - criar palavras no banco de dados;
        - controlar quais campos serão expostos.
    """

    created_by = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    
    class Meta:
        model = Word
        fields = ['word', 'meaning', 'example', 'created_by']
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