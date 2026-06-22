from rest_framework.serializers import ModelSerializer
from ..models import Word

from rest_framework import serializers

class WordSerializerV3(ModelSerializer):
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
        fields = ['word', 'meaning', 'example', 'created_by', 'created_at', 'updated_at']
        read_only_fields = [
            'created_by',
            'created_at',
            'updated_at'
        ]
    
    def validate_word(self, value):

        if value.isdigit():
            raise serializers.ValidationError(
                'Uma palavra não pode conter apenas números.'
            )
        return value

    def validate_meaning(self, value):
        
        if value.isdigit():
            raise serializers.ValidationError(
                'O significado não pode conter apenas números.'
            )
        
        return value