from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word

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
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        # self.assertEqual(response.data['message'], 'Login realizado com sucesso')

    
    def test_login_invalid_credentials_wrong_username(self):

        User.objects.create_user(
            username='nome',
            password='12356'
        )

        data = {
            'username': 'outro-nome',
            'password': '123456'
        }
        response = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Credenciais inválidas')
        self.assertEqual(response.data['detail'].code, 'authentication_failed')

    
    def test_login_invalid_credentials_wrong_password(self):

        User.objects.create_user(
            username='nome',
            password='12356'
        )

        data = {
            'username': 'outro-nome',
            'password': 'abcde'
        }
        response = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Credenciais inválidas')
        self.assertEqual(response.data['detail'].code, 'authentication_failed')

    
    def test_login_with_nonexistent_user(self):
        
        data = {
            'username': 'outro-nome',
            'password': 'abcde'
        }
        response = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response.status_code, 403)

    
    def test_login_without_username(self):

        data = {
            'password': 'abcde'
        }
        response = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], 'This field is required.')


    
    def test_login_without_password(self):

        data = {
            'username': 'outro-nome'
        }
        response = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], 'This field is required.')

    
    def test_token_is_created(self):
        user = User.objects.create_user(
            username='nome',
            email='okokokoko',
            password='12345'
        )
        data = {
            'username': 'nome',
            'password': '12345'
        }
        self.client.post(reverse('login-v2'), data=data)
        self.assertTrue(Token.objects.filter(user=user).exists())

    
    def test_multiple_logins_use_same_token(self):
        user = User.objects.create_user(
            username='nome',
            email='blblbl',
            password='12345'
        )

        data = {
            'username': 'nome',
            'password': '12345'
        }
        response1 = self.client.post(reverse('login-v2'), data=data)
        response2 = self.client.post(reverse('login-v2'), data=data)
        self.assertEqual(response1.data['token'], response2.data['token'])
        self.assertEqual(Token.objects.filter(user=user).count(), 1)


    
class TestLogoutViewV2(APITestCase):
    
    def test_logout_success(self):
        
        user = User.objects.create_user(
            username='nome',
            password='12345'
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(reverse('logout-v2'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Logout realizado com sucesso')
        self.assertFalse(Token.objects.filter(user=user).exists())

    
    def test_unauthenticated_user_cannot_logout(self):
        response = self.client.post(reverse('logout-v2'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    
    def test_logout_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token token_inexistente')
        response = self.client.post(reverse('logout-v2'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        self.assertEqual(response.data['detail'].code, 'authentication_failed')

    
    def test_cannot_use_deleted_token(self):
        user = User.objects.create_user(
            username='nome',
            password='12345'
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        self.client.post(reverse('logout-v2'))
        response = self.client.post(reverse('logout-v2'))
        response = self.client.post(reverse('logout-v2'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid token.')



class TestListWordsView(APITestCase):

    def test_anyone_can_list_words(self):

        Word.objects.create(
            word='python',
            meaning='linguagem'
        )

        response = self.client.get(reverse('words-v2'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn('example', response.data[0])


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
        self.assertIn('example', response.data)

    
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



class TestUpdateWordView(APITestCase):

    def test_admin_can_update_word_partially(self):
        admin = User.objects.create_superuser(
            username='cabral',
            password='12345'
        )
        word = Word.objects.create(
            word='palavra',
            meaning='antigo significado',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(reverse('update-word-v2', kwargs={'word': 'palavra'}), {'meaning': 'novo significado'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['meaning'], 'novo significado')
        word.refresh_from_db()
        self.assertEqual(word.meaning, 'novo significado')

    
    def test_admin_can_update_word_totally(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='palavra',
            meaning='antigo significado',
            example='old example',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.put(reverse('update-word-v2', kwargs={'word': 'palavra'}), {'word': 'outra', 'meaning': 'novo significado', 'example': 'new example'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'outra')
        self.assertEqual(response.data['meaning'], 'novo significado')
        self.assertEqual(response.data['example'], 'new example')
        word.refresh_from_db()
        self.assertEqual(word.word, 'outra')
        self.assertEqual(word.meaning, 'novo significado')
        self.assertEqual(word.example, 'new example')


    def test_admin_update_word_invalid_type(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='palavra',
            meaning='antigo significado',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(reverse('update-word-v2', kwargs={'word': 'palavra'}), {'meaning': 56565})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'O significado não pode conter apenas números.')
        self.assertNotEqual(word.meaning, 56565)


    def test_admin_update_word_missing_fields(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        word = Word.objects.create(
            word='palavra',
            meaning='antigo significado',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.patch(reverse('update-word-v2', kwargs={'word': 'palavra'}), {'meaning': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'This field may not be blank.')


    def test_non_authorized_user_cannot_update_word(self):
        user = User.objects.create_user(
            username='normal_user',
            password='12345'
        )
        word = Word.objects.create(
            word='word',
            meaning='...'
        )

        self.client.force_authenticate(user=user)
        response = self.client.patch(reverse('update-word-v2', kwargs={'word': 'word'}), {'meaning': 'nvovo significado'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(response.data['detail'].code, 'permission_denied')



class TestDeleteWordView(APITestCase):

    def test_admin_can_delete_word(self):
        
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        Word.objects.create(
            word='word',
            meaning='...',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.delete(reverse('delete-word-v2', kwargs={'word': 'word'}))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertFalse(Word.objects.filter(word='word').exists())

    
    def test_delete_word_not_found(self):

        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        Word.objects.create(
            word='word',
            meaning='...',
            created_by=admin
        )

        self.client.force_authenticate(user=admin)

        response = self.client.delete(reverse('delete-word-v2', kwargs={'word': 'nada'}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Word.objects.filter(word='word').exists())
        self.assertEqual(response.data['detail'], 'No Word matches the given query.')
        self.assertEqual(response.data['detail'].code, 'not_found')

    
    def test_non_admin_cannot_delete_word(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='12345'
        )
        user = User.objects.create_user(
            username='user',
            password='54321'
        )

        Word.objects.create(
            word='word',
            meaning='...',
            created_by=admin
        )

        self.client.force_authenticate(user=user)

        response = self.client.delete(reverse('delete-word-v2', kwargs={'word': 'word'}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')