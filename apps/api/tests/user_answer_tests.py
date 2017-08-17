import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, Page, Favorite
from apps.question.models import Question, Answer, UserAnswer
from apps.userprofile.models import User


client = Client()


class UserAnswerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.question = Question.objects.create(question_text='some random text', is_published=True, 
                                                lesson=self.lesson)
        self.answer = Answer.objects.create(text='answer text', is_valid=True, is_active=True, question=self.question)
        self.user_answer = UserAnswer.objects.create(user=self.user, question=self.question, correct=True)

    def test_user_answer_create(self):
        response = client.post('/api/user_answer/', 
                               json.dumps(
                               { 
                                   'user': self.user.id, 
                                   'question': self.question.id,
                                   'correct': True
                               }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_answer_detail(self):
        response = client.get('/api/user_answer/{}/'.format(self.user_answer.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_answer_list(self):
        response = client.get('/api/user_answer/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_answer_update(self):
        question = Question.objects.create(question_text='new random text', is_published=True, lesson=self.lesson)
        response = client.put('/api/user_answer/{}/'.format(self.question.id), 
                              json.dumps(
                              { 
                                  'user': self.user.id, 
                                  'question': self.question.id,
                                  'correct': True
                              }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_answer_delete(self):
        question = Question.objects.create(question_text='new random text', is_published=True, lesson=self.lesson)
        response = client.put('/api/user_answer/{}/'.format(self.question.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
