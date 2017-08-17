import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.api.serializers.userprofile import UserSerializer
from apps.lesson.models import LessonSet, Lesson, Page, Favorite
from apps.question.models import Question
from apps.userprofile.models import User


client = Client()


class QuestionTest(TestCase):

    def setUp(self):
        user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.question = Question.objects.create(question_text='some random text', is_published=True, 
                                                lesson=self.lesson)

    def test_question_create(self):
        response = client.post('/api/question/', 
                               json.dumps(
                               { 
                                   'question_text': 'question text', 
                                   'is_published': True,
                                   'lesson': self.lesson.id 
                               }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_question_detail(self):
        response = client.get('/api/question/{}/'.format(self.question.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_list(self):
        response = client.get('/api/question/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_question_update(self):
        lesson = Lesson.objects.create(topic='new lesson topic', lesson_set=self.lessonset)
        response = client.put('/api/question/{}/'.format(self.question.id), 
                              json.dumps(
                              { 
                                  'question_text': 'new question text', 
                                  'is_published': False,
                                  'lesson': lesson.id 
                              }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_delete(self):
        response = client.delete('/api/question/{}/'.format(self.question.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
