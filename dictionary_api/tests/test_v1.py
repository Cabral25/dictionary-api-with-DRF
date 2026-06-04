from rest_framework.test import APITestCase
from django.urls import reverse

from dictionary_api.models import Word


class ListWordTests(APITestCase):
    
    def test_anyone_can_list_words(self):

        Word.objects.create(
            word='python',
            meaning='linguagem'
        )

        response = self.client.get(reverse('words'))

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data), 1)