from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        Modelo de usuário customizado da aplicação.

        Este model herda de AbstractUser, uma classe do Django
        que já implementa um sistema completo de autenticação.

        Ao herdar de AbstractUser, o model já recebe automaticamente
        diversos campos e funcionalidades importantes, como:

        - username
        - password
        - email
        - first_name
        - last_name
        - is_staff
        - is_superuser
        - is_active
        - date_joined
        - last_login

        Funcionalidades automáticas:
        - autenticação
        - hash seguro de senhas
        - permissões
        - grupos
        - login/logout
        - integração com painel admin
        - controle de usuários administradores

        A utilização de AbstractUser permite customizar o usuário
        da aplicação sem precisar reimplementar todo o sistema
        de autenticação do Django.
    """

    class Meta:

        verbose_name = 'User'

        verbose_name_plural = 'Users'


    def __str__(self):
        return self.username



class Word(models.Model):
    word_id = models.IntegerField()
    word = models.CharField(unique=True)
    meaning = models.TextField()
    example = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add define a data/hora apenas uma vez: no momento de criar o objeto
    updated_at = models.DateTimeField(auto_now=True) # auto_now atualiza toda vez que o objeto é salvo

    def __str__(self):
        return self.word

# Create your models here.
