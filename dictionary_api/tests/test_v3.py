from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django.urls import reverse
from django.contrib.auth import get_user_model

from dictionary_api.models import Word


User = get_user_model()



class TestLoginViewV3(APITestCase):
    
    def test_login_returns_access_and_refresh_tokens(self):

        User.objects.create_user(
            username='admin',
            password='12345'
        )

        data = {
            'username': 'admin',
            'password': '12345'
        }
        response = self.client.post(reverse('login-v3'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    
    def test_login_returns_valid_jwt_tokens(self):

        User.objects.create_user(
            username='admin',
            password='12345'
        )

        data = {
            'username': 'admin',
            'password': '12345'
        }
        response = self.client.post(reverse('login-v3'), data=data)
        access_token = AccessToken(response.data['access'])
        refresh_token = RefreshToken(response.data['refresh'])
        print(response.data)
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

    
    def test_login_with_wrong_password(self):

        User.objects.create_user(
            username='admin',
            password='12345'
        )

        data = {
            'username': 'admin',
            'password': 'senha_errada'
        }
        response = self.client.post(reverse('login-v3'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Credenciais inválidas')

    
    def test_login_without_username(self):

        data = {
            'password': '12345'
        }
        response = self.client.post(reverse('login-v3'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0], 'This field is required.')

    
    def test_login_without_password(self):

        data = {
            'username': 'admin',
        }
        response = self.client.post(reverse('login-v3'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], 'This field is required.')

    
    def test_tokens_belong_to_correct_user(self):

        user = User.objects.create_user(
            username='admin',
            password='12345'
        )

        data = {
            'username': 'admin',
            'password': '12345'
        }
        response = self.client.post(reverse('login-v3'), data=data)
        access_token = AccessToken(response.data['access'])
        print(response.data)
        self.assertEqual(int(access_token['user_id']), user.id)

    
    def test_access_token_can_authenticate_user(self):

        user = User.objects.create_user(
            username='admin',
            password='12345'
        )

        data = {
            'username': 'admin',
            'password': '12345'
        }
        login_response = self.client.post(reverse('login-v3'), data=data)
        access_token = login_response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        response = self.client.get(reverse('list-words-v3'))
        print(response.data)
        self.assertEqual(response.status_code, 200)



class TestLogoutViewV3(APITestCase):
    
    def test_autheticated_user_can_logout(self):

        user = User.objects.create_user(
            username='admin',
            password='12345'
        )
        
        self.client.force_authenticate(user=user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )

        data = {
            'refresh': str(refresh)
        }
        response = self.client.post(reverse('logout-v3'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)



class TestRefreshView(APITestCase):
    pass



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
        response = self.client.post(reverse('list-words-v3'), data=data)
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
        response = self.client.post(reverse('list-words-v3'), data=data)
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
        response = self.client.post(reverse('list-words-v3'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'This field is required.')
        self.assertEqual(response.request['PATH_INFO'], '/api/v3/words/')
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
        response = self.client.post(reverse('list-words-v3'), data=data)
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
        response = self.client.post(reverse('list-words-v3'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['meaning'][0], 'O significado não pode conter apenas números.')



class TestDetailWordView(APITestCase):
    
    def test_any_user_can_get_existing_word_success(self):
        word = Word.objects.create(
            word='palavra',
            meaning='menor unidade de uma língua'
        )
        response = self.client.get(reverse('word-detail-v3', kwargs={'word': 'palavra'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'palavra')

    
    def test_get_inexistent_word(self):

        response = self.client.get(reverse('word-detail-v3', kwargs={'word': 'java'}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No Word matches the given query.')
        self.assertEqual(response.data['detail'].code, 'not_found')

    
    def test_lookup_is_performed_using_word_field(self):

        Word.objects.create(
            word='palavra',
            meaning='any meaning'
        )

        response = self.client.get(reverse('word-detail-v3', kwargs={'word': 'palavra'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['word'], 'palavra')

    
    def test_response_contains_expected_fields(self):
        admin = User.objects.create_user(
            username='admin',
            password='12345'
        )

        Word.objects.create(
            word='python',
            meaning='Linguagem',
            created_by=admin
        )

        response = self.client.get(reverse('word-detail-v3', kwargs={'word': 'python'}))
        print(response.data)
        self.assertIn('word', response.data)
        self.assertIn('meaning', response.data)
        self.assertIn('example', response.data)
        self.assertIn('created_by', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)



class TestSearchWordView(APITestCase):

    def test_search_returns_matching_words(self):

        for i in range(5):
            Word.objects.create(
                word=f'casa{i}',
                meaning=f'meaning{i}'
            )

        data = {'q': 'CASA'}
        response = self.client.get(reverse('search-word-v3'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    
    def test_search_returns_no_matching_words(self):

        Word.objects.create(
            word='casa',
            meaning='...'
        )

        data = {'q': 'ruby'}
        response = self.client.get(reverse('search-word-v3'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    
    def test_search_without_query_returns_empty_queryset(self):

        response = self.client.get(reverse('search-word-v3'))
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

        response = self.client.patch(reverse('update-word-v3', kwargs={'word': 'palavra'}), {'meaning': 'novo significado'})
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

        response = self.client.put(reverse('update-word-v3', kwargs={'word': 'palavra'}), {'word': 'outra', 'meaning': 'novo significado', 'example': 'new example'})
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

        response = self.client.patch(reverse('update-word-v3', kwargs={'word': 'palavra'}), {'meaning': 56565})
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

        response = self.client.patch(reverse('update-word-v3', kwargs={'word': 'palavra'}), {'meaning': ''})
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
        response = self.client.patch(reverse('update-word-v3', kwargs={'word': 'word'}), {'meaning': 'nvovo significado'})
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

        response = self.client.delete(reverse('delete-word-v3', kwargs={'word': 'word'}))
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

        response = self.client.delete(reverse('delete-word-v3', kwargs={'word': 'nada'}))
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

        response = self.client.delete(reverse('delete-word-v3', kwargs={'word': 'word'}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')