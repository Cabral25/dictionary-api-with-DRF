from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word
from dictionary_api.v1.serializers import LoginSerializer


User = get_user_model()


class LoginViewTest(APITestCase):
    
    def test_login_valid_credentials(self):
        user = User.objects.create_user(
            username='nome',
            password='12345'
        )

        data = {
            'username': 'nome',
            'password': '12345'
        }
        
        response = self.client.post(reverse('login-v1'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Login realizado com sucesso')

    
    def test_login_invalid_credentials(self):

        User.objects.create_user(
            username='nome',
            password='12345'
        )

        data = {
            'username': 'nome',
            'password': '54321'
        }
        response = self.client.post(reverse('login-v1'), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Credenciais inválidas')

    
    def test_login_with_nonexistent_user(self):

        data = {
            'username': 'nome',
            'password': '54321'
        }
        response = self.client.post(reverse('login-v1'), data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Credenciais inválidas')

    
    def test_session_is_created_after_login(self):

        User.objects.create_user(
            username='nome',
            password='12345'
        )

        data = {
            'username': 'nome',
            'password': '12345'
        }
        response = self.client.post(reverse('login-v1'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    
    def test_login_serializer_requires_username(self):

        serializer = LoginSerializer(
            data={
                'password': '12345'
            }
        )
        self.assertFalse(serializer.is_valid())

    
    def test_login_serializer_requires_password(self):

        serializer = LoginSerializer(
            data={
                'username': 'nome'
            }
        )
        self.assertFalse(serializer.is_valid())



class LogoutViewTests(APITestCase):
    
    def test_authenticated_user_can_logout(self):
        user = User.objects.create_user(
            username='nome',
            password='12345'
        )

        self.client.force_login(user)

        response = self.client.post(reverse('logout-v1'))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Logout realizado com sucesso')

    
    def test_anonymous_user_cannot_logout(self):
        response = self.client.post(reverse('logout-v1'))
        print(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')



class ListCreateWordTests(APITestCase):
    
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
        print(response.data)
        self.assertEqual(response.status_code, 403)
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
        response = self.client.post(reverse('words'), data=data)
        print(response.data)
        print('status: ', response.status_code)
        print(response.request['REQUEST_METHOD'], response.request['PATH_INFO'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'This field is required.')
        self.assertEqual(response.request['PATH_INFO'], '/api/v1/words/')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')

    
    def test_invalid_data_type(self):
        user = User.objects.create_superuser(
            username='admin123',
            password='anypassword321',
            email='any@email.com'
        )

        self.client.force_authenticate(user=user)
        data = {
            'word': 90909,
            'meaning': 'framework'
        }
        response = self.client.post(reverse('words'), data=data)
        print(response.data)
        print('status: ', response.status_code)
        self.assertEqual(response.status_code, 400)



class DetailWordViewTest(APITestCase):
    
    def test_get_existing_word_success(self):
        word = Word.objects.create(
            word='palavra',
            meaning='menor unidade de uma língua'
        )
        response = self.client.get(reverse('word-detail-v1', kwargs={'word': 'palavra'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'palavra')
        self.assertIn('word', response.data)
        self.assertIn('meaning', response.data)

    
    def test_get_inexistent_word(self):
        response = self.client.get(reverse('word-detail-v1', kwargs={'word': 'java'}))
        self.assertEqual(response.status_code, 404)

    
    def test_anonymous_user_can_access_detail_view(self):

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

        self.assertEqual(
            response.status_code,
            200
        )

    
    def test_lookup_is_performed_using_word_field(self):

        Word.objects.create(
            word='palavra',
            meaning='any meaning'
        )

        response = self.client.get(reverse('word-detail-v1', kwargs={'word': 'palavra'}))
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



class SearchWordViewTests(APITestCase):
    
    def test_search_returns_matching_words(self):

        Word.objects.create(
            word='python',
            meaning='...'
        )

        data = {'q': 'python'}
        response = self.client.get(reverse('search-word-v1'), data=data)
        print(response.data)
        print(response.request['PATH_INFO'])
        print('status: ', response.status_code)
        self.assertEqual(response.status_code, 200)



class UpdateWordViewTests(APITestCase):
    pass



class DeleteWordViewTests(APITestCase):
    pass