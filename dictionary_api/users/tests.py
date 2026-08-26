from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class TestsUserCreateView(APITestCase):

    def test_user_is_created_with_valid_data(self):
        data = {
            'username': 'user',
            'password': 12345,
            'email': 'a@gmail.com'
        }
        response = self.client.post(reverse('register'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)