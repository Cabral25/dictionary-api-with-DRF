from rest_framework.serializers import ModelSerializer
from .models import User, Word


class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'



class WordSerializer(ModelSerializer):
    
    class Meta:
        model = Word
        fields = '__all__'