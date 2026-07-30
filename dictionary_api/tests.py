from django.test import TestCase
from .models import User, Word
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

import time

Usuario = get_user_model()


# Testes dos models

class UserModelTeste(TestCase):

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
        old_updated = word.updated_at
        time.sleep(1)
        word.meaning = 'novo significado'
        word.save()

        self.assertIsNotNone(word.created_at)
        self.assertGreater(word.updated_at, old_updated)


    def test_word_must_be_unique(self):

        user = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='word',
            meaning='...',
            created_by=user
        )

        with self.assertRaises(IntegrityError):
            word = Word.objects.create(
                word='word',
                meaning='...',
                created_by=user
            )


    def test_created_by_becomes_null_when_deleted(self):

        user = User.objects.create_superuser(
            username='admin',
            password='12345'
                )
        word = Word.objects.create(
            word='word',
            meaning='...',
            created_by=user
                )

        user.delete()
        word.refresh_from_db()
        self.assertIsNone(word.created_by)


# Testes dos serializers


class UserSerializerTest(TestCase):
    pass



class WordSerializerTest(TestCase):
    pass


# Create your tests here.
