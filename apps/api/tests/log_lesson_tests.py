import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, LogLesson
from apps.userprofile.models import User


client = Client()


class LogLessonTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.log_lesson = LogLesson.objects.create(user=self.user, lesson=self.lesson, is_viewed=True)
   
    def test_log_lesson_create(self):
        response = client.post('/api/log_lesson/', 
                               json.dumps({ 
                                   'user': self.user.id, 
                                   'lesson': self.lesson.id,
                                   'is_viewed': True
                               }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_log_lesson_detail(self):
        response = client.get('/api/log_lesson/{}/'.format(self.log_lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_log_lesson_list(self):
        response = client.get('/api/log_lesson/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_log_lesson_delete(self):
        response = client.delete('/api/log_lesson/{}/'.format(self.log_lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
