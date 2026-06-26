from django.test import TestCase
from .models import User, Word
from django.db.utils import IntegrityError


# Testes dos models

class UserModelTeste(TestCase):
    
    def test_user_is_created_successfully(self):
        pass



class WordModelTest(TestCase):
    
    def test_word_is_created_successfully(self):
        pass


# Testes dos serializers


class UserSerializerTest(TestCase):
    pass



class WordSerializerTest(TestCase):
    pass


# Create your tests here.
