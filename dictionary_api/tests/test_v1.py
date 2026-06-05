from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word

User = get_user_model()


class ListWordTests(APITestCase):
    
    def test_anyone_can_list_words(self):

        Word.objects.create(
            word='python',
            meaning='linguagem'
        )

        response = self.client.get(reverse('words'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


    def test_anonymous_user_cannot_create_word(self):
        data = {
            'word': 'django',
            'meaning': 'framework'
        }
        response = self.client.post(reverse('words'), data=data)
        self.assertEqual(response.status_code, 403)


    def test_admin_can_create_word(self):
        admin = User.objects.create_superuser(
            username='cabral',
            email='adecabral673@gmail.com',
            password='65321'
        )

        self.client.force_authenticate(user=admin)

        data = {
            'word': 'django',
            'meaning': 'framework'
        }
        response = self.client.post(reverse('words'), data=data)
        print('status_code:', response.status_code)
        print('número de objetos criados', Word.objects.count())
        print('objeto criado: ', response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Word.objects.count(), 1)


    def test_logged_user_cannot_create_word(self):
        user = User.objects.create_user(
            username='admin123',
            password='anypassword321',
            email='any@email.com'
        )

        self.client.force_authenticate(user=user)
        data = {
            'word': 'django',
            'meaning': 'framework'
        }
        response = self.client.post(reverse('words'), data=data)
        print('status code:', response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{"detail":"You do not have permission to perform this action."}')