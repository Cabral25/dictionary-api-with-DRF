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