from rest_framework.serializers import ModelSerializer
from .models import User, Word

"""
    O serializer é uma das partes mais importantes do DRF.
    Ele é responsável por converter objetos Python em JSON
    e converter JSON em objetos Python, então:

        user = User.objects.get(id=1) <-- objeto Python

    vira:

        {
            'id': 1,
            'username': 'nome',           <-- JSON
            'email': 'oioi@gmail.com'
        }

    O serializer também é responsável pela validação de dados.
    No exemplo acima, o serializer valida os dados e cria um
    objeto User.
    Também serve pra controlar o que será exposto na API.
    Por exemplo:

        você NÃO quer retornar senha;
        talvez não queira mostrar email;
        talvez admin veja campos diferentes.

    No serializer UserSerializer, por exemplo, a configuração
    extra_kwargs garante que a senha pode ser enviada mas
    nunca será retornada.

"""


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
        fields = ['id', 'username', 'password', 'email', 'is_staff', 'is_superuser', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }



class WordSerializer(ModelSerializer):
    
    class Meta:
        model = Word
        fields = '__all__'
        read_only_fields = [
            'created_by',
            'created_at',
            'updated_at'
        ]