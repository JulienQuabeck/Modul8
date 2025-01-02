from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from forum_app.models import Question, Like
from django.contrib.auth.models import User
from forum_app.api.serializers import QuestionSerializer
from rest_framework.authtoken.models import Token


class LikeTests(APITestCase):

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
