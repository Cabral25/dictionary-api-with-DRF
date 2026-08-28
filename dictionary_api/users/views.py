from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from ..models import User
from .serializers import UserSerializer


"""
    Views referentes aos usuários.
"""


class UserCreateView(CreateAPIView):
    """
        View para o registro de novos usuários.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]