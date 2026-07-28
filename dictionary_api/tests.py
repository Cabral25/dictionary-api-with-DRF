from django.test import TestCase
from .models import User, Word
from django.db.utils import IntegrityError


# Testes dos models

class UserModelTeste(TestCase):
    
    def test_user_is_created_successfully(self):
        pass


    def test_user_str_returns_username(self):
        user = User.objects.create_user(
            username='user',
            password='12345'
        )
        self.assertEqual(str(user), 'user')


    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )

        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)



class WordModelTest(TestCase):
    
    def test_word_is_created_successfully(self):
        pass


    def test_word_str_returns_word(self):
        user = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='word',
            meaning='...',
            created_by=user
        )

        self.assertEqual(str(word), 'word')

    
    def test_automatic_fields_are_set(self):
        user = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='word',
            meaning='...',
            created_by=user
        )


# Testes dos serializers


class UserSerializerTest(TestCase):
    pass



class WordSerializerTest(TestCase):
    pass


# Create your tests here.
