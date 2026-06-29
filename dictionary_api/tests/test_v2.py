from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word
from dictionary_api.v1.serializers import LoginSerializer

User = get_user_model()



class TestLoginViewV2(APITestCase):
    
    def test_login_valid_credentials(self):
        user = User.objects.create_user(
            username='nome',
            password='12345'
        )

        data = {
            'username': 'nome',
            'password': '12345'
        }
        
        response = self.client.post(reverse('login-v2'), data=data)
        print(response.data)
        print(response.request)
        print('status:', response.status_code)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['message'], 'Login realizado com sucesso')

    
class TestLogoutViewV2(APITestCase):
    pass



class TestListWordsView(APITestCase):

    def test_anyone_can_list_words(self):

        Word.objects.create(
            word='python',
            meaning='linguagem'
        )

        response = self.client.get(reverse('words-v2'))
        print('data:', response.data)
        print('request:', response.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn('example', response.data[0])
        self.assertIn('created_by', response.data[0])


    def test_anonymous_user_cannot_create_word(self):
        data = {
            'word': 'django',
            'meaning': 'framework'
        }
        response = self.client.post(reverse('words-v2'), data=data)
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
        word = Word.objects.first()
        print(admin)
        print('data:', response.data)
        print('request:', response.request)
        print('criado por:', word.created_by)
        print('id autor:', word.created_by_id)
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
        self.assertEqual(response.content, b'{"detail":"You do not have permission to perform this action."}')

    
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



class TestDetailWordView(APITestCase):
    
    def test_any_user_can_get_existing_word_success(self):
        word = Word.objects.create(
            word='palavra',
            meaning='menor unidade de uma língua'
        )
        response = self.client.get(reverse('word-detail-v2', kwargs={'word': 'palavra'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'palavra')
        self.assertIn('word', response.data)
        self.assertIn('meaning', response.data)

    
    def test_get_inexistent_word(self):

        response = self.client.get(reverse('word-detail-v2', kwargs={'word': 'java'}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No Word matches the given query.')
        self.assertEqual(response.data['detail'].code, 'not_found')

    
    def test_lookup_is_performed_using_word_field(self):

        Word.objects.create(
            word='palavra',
            meaning='any meaning'
        )

        response = self.client.get(reverse('word-detail-v2', kwargs={'word': 'palavra'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'palavra')

    
    def test_response_contains_expected_fields(self):

        Word.objects.create(
            word='python',
            meaning='Linguagem'
        )

        response = self.client.get(
            reverse(
                'word-detail-v1',
                kwargs={'word': 'python'}
            )
        )

        self.assertIn(
            'word',
            response.data
        )
        self.assertIn(
            'meaning',
            response.data
        )
        self.assertNotIn('example', response.data)
        self.assertNotIn('created_by', response.data)



class TestSearchWordView(APITestCase):

    def test_search_returns_matching_words(self):

        for i in range(5):
            Word.objects.create(
                word=f'casa{i}',
                meaning=f'meaning{i}'
            )

        data = {'q': 'CASA'}
        response = self.client.get(reverse('search-word-v2'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    
    def test_search_returns_no_matching_words(self):

        Word.objects.create(
            word='casa',
            meaning='...'
        )

        data = {'q': 'ruby'}
        response = self.client.get(reverse('search-word-v2'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    
    def test_search_without_query_returns_empty_queryset(self):

        response = self.client.get(reverse('search-word-v2'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.request['QUERY_STRING'], '')