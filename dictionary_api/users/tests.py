from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class TestsUserCreateView(APITestCase):

    def test_user_is_created_with_valid_data(self):
        data = {
            'username': 'user____',
            'password': 12345678,
            'email': 'a@gmail.com'
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 201)


    def test_password_is_not_returned(self):
        data = {
            'username': 'joao_homem',
            'password': 'SenhaForte123!',
            'email': 'joao@email.com',
    }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)


    def test_password_is_hashed(self):
        data = {
            'username': 'user___-',
            'password': 12345678,
            'email': 'a@gmail.com'
        }

        self.client.post(reverse('register'), data)
        user = User.objects.get(username='user___-')
        self.assertNotEqual(user.password, 'SenhaForte123!')
        self.assertTrue(user.check_password('12345678'))

    
    def test_duplicate_username(self):
        User.objects.create_user(
            username='joao_homem',
            password='SenhaForte123!'
        )

        data = {
            'username': 'joao_homem',
            'password': 'OutraSenha123!',
            'email': 'outro@email.com',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')


    def test_username_is_required(self):
        data = {
            'password': 'SenhaForte123!',
            'email': 'joao@email.com',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0], 'This field is required.')


    def test_password_is_required(self):
        data = {
            'username': 'joao_hmem',
            'email': 'joao@email.com',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], 'This field is required.')


    def test_password_too_short(self):
        data = {
            'username': 'joao_homem',
            'password': '123',
            'email': 'joao@email.com',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], 'A senha deve possuir pelo menos 8 caracteres.')


    def test_username_too_short(self):
        data = {
                'username': 'joao',
                'password': '12345678',
                'email': 'joao@email.com',
            }
    
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0], 'O username deve possuir pelo menos 8 caracteres.')


    def test_invalid_email(self):
        data = {
            'username': 'joao_homem',
            'password': 'SenhaForte123!',
            'email': 'email_invalido',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')