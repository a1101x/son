import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, Page, Favorite
from apps.question.models import Question, Answer
from apps.userprofile.models import User


client = Client()


class AnswerTest(TestCase):

    def setUp(self):
        user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.question = Question.objects.create(question_text='some random text', is_published=True, 
                                                lesson=self.lesson)
        self.answer = Answer.objects.create(text='answer text', is_valid=True, is_active=True, question=self.question)

    def test_answer_create(self):
        response = client.post('/api/answer/', 
                               json.dumps(
                               { 
                                   'text': 'new answer text', 
                                   'is_valid': False,
                                   'is_active': True,
                                   'question': self.question.id 
                               }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_answer_detail(self):
        response = client.get('/api/answer/{}/'.format(self.answer.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_list(self):
        response = client.get('/api/answer/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_update(self):
        question = Question.objects.create(question_text='new random text', is_published=True, lesson=self.lesson)
        response = client.put('/api/answer/{}/'.format(self.question.id), 
                              json.dumps(
                              { 
                                  'text': 'yet another new answer text', 
                                  'is_valid': True,
                                  'is_active': False,
                                  'question': question.id 
                              }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_delete(self):
        response = client.delete('/api/answer/{}/'.format(self.question.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_admin(self):
        user = User.objects.create_user(email='user@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        auth = 'JWT {}'.format(token)
        response = client.post('/api/answer/', 
                               json.dumps(
                               { 
                                   'text': 'new answer text', 
                                   'is_valid': False,
                                   'is_active': True,
                                   'question': self.question.id 
                               }), content_type='application/json', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
