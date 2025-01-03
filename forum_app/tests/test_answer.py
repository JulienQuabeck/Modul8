from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from forum_app.models import Question, Answer
from django.contrib.auth.models import User
from forum_app.api.serializers import QuestionSerializer, AnswerSerializer
from rest_framework.authtoken.models import Token

class AnswerTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.question = Question.objects.create(
            title='Test Question', 
            content='Test Content', 
            author=self.user, 
            category='frontend'
        )

        self.answer = Answer.objects.create(content='Test Answer', author=self.user, question=self.question)

        self.token =  Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_answer_get(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_detail(self):
        url = reverse('answer-detail', kwargs={'pk' : self.answer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_answer_post(self):
        url = reverse('answer-list-create')
        data = {
            'question':self.question.id,
            'content':'1Answer',
            'author': self.user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_answer_update_authorized(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        updated_data = {
            'question':self.question.id,
            'content': 'Updated Answer Content',
            'author': self.user.id,
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_update_unauthorized(self):
        self.client.logout()
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)
        
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        updated_data = {
            'content': 'Updated Answer Content'
        }
        
        response = other_client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_answer_delete(self):
        url = reverse('answer-detail', kwargs={'pk' : self.answer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 
