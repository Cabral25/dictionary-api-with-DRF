from django.test import TestCase
from django.urls import reverse



class TestsUserCreateView(TestCase):

    def test_user_is_created_with_valid_data(self):
        data = {
            'username': 'user',
            'password': 12345
        }
        response = self.client.post(reverse('register'), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)