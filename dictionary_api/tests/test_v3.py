from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word


User = get_user_model()



class TestListWordsV3(APITestCase):

    def test_anyone_can_access_words(self):
        Word.objects.create(
            word='word',
            meaning='meaning',
        )
        response = self.client.get(reverse('list-words-v3'))
        print(response.data)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertIn('example', response.data[0])
        self.assertIn('created_at', response.data[0])
        self.assertIn('updated_at', response.data[0])

    
    def test_anonymous_user_cannot_create_word(self):
        data = {
            'word': 'django',
            'meaning': 'framework'
        }
        response = self.client.post(reverse('list-words-v3'), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


    def test_admin_can_create_word(self):
        admin = User.objects.create_superuser(
            username='cabral',
            email='adecabral673@gmail.com',
            password='65321'
        )

        self.client.force_authenticate(user=admin)

        data = {
            'word': 'django',
            'meaning': 'framework',
        }
        response = self.client.post(reverse('words-v2'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Word.objects.count(), 1)
        self.assertEqual(response.data['created_by'], 'cabral')


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
        response = self.client.post(reverse('words-v2'), data=data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "You do not have permission to perform this action.")
        self.assertEqual(response.data['detail'].code, 'permission_denied')

    
    def test_missing_required_fields(self):

        user = User.objects.create_superuser(
            username='admin123',
            password='anypassword321',
            email='any@email.com'
        )

        self.client.force_authenticate(user=user)
        data = {
            'word': 'django',
        }
        response = self.client.post(reverse('words-v2'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'This field is required.')
        self.assertEqual(response.request['PATH_INFO'], '/api/v2/words/')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')

    
    def test_create_word_with_invalid_data_type_word(self):
        user = User.objects.create_superuser(
            username='admin123',
            password='anypassword321',
            email='any@email.com'
        )

        self.client.force_authenticate(user=user)
        data = {
            'word': 90909,
            'meaning': 'número'
        }
        response = self.client.post(reverse('words-v2'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['word'][0], 'Uma palavra não pode conter apenas números.')

    
    def test_create_word_with_invalid_data_type_meaning(self):
        user = User.objects.create_superuser(
            username='admin123',
            password='anypassword321',
            email='any@email.com'
        )

        self.client.force_authenticate(user=user)
        data = {
            'word': 'casa',
            'meaning': 55555
        }
        response = self.client.post(reverse('words-v2'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'O significado não pode conter apenas números.')