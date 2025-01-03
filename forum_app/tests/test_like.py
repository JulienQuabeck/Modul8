from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from forum_app.models import Question, Like
from django.contrib.auth.models import User
from forum_app.api.serializers import QuestionSerializer
from rest_framework.authtoken.models import Token


class LikeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(
            title='Test Question', 
            content='Test Content', 
            author=self.user, 
            category='frontend'
        )
        self.token =  Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_detail(self):
        self.like = Like.objects.create(user=self.user, question=self.question)
        url = reverse('like-detail', kwargs={'pk' : self.like.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_like_post(self):
        url = reverse('like-list')
        data = {
            'question': self.question.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_like_delete(self):
        self.like = Like.objects.create(user=self.user, question=self.question)
        url = reverse('like-detail', kwargs={'pk' : self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 
