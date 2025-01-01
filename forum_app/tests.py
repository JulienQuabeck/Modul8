from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class LikeTests(APITestCase):

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_answer(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)