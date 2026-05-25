from rest_framework.serializers import ModelSerializer
from .models import User, Words


class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'



class WordSerializer(ModelSerializer):
    
    class Meta:
        model = Words
        fields = '__all__'