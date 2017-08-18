import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, Page
from apps.userprofile.models import User


client = Client()
    

class LessonTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
   
    def test_lesson_create(self):
        lesson1 = client.post('/api/lesson/', json.dumps({ 'topic': 'topic1', 'lesson_set': self.lessonset.id }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(lesson1.status_code, status.HTTP_201_CREATED)
        lesson2 = client.post('/api/lesson/', json.dumps({ 'topic': 'topic2', 'lesson_set': self.lessonset.id }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(lesson2.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        lessonset2 = LessonSet.objects.create(topic='another lesson set topic')
        response = client.put('/api/lesson/{}/'.format(self.lesson.id), 
                              json.dumps({ 
                                  'topic': 'topic1234', 
                                  'description': 'desc123232', 
                                  'lesson_set': lessonset2.id 
                              }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_detail(self):
        response = client.get('/api/lesson/{}/'.format(self.lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_list(self):
        response = client.get('/api/lesson/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        response = client.delete('/api/lesson/{}/'.format(self.lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_lesson_pages(self):
        page = Page.objects.create(lesson=self.lesson, text='text')
        response = client.get('/api/lesson/{}/pages/'.format(self.lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_copy(self):
        response = client.post('/api/lesson/{}/copy/'.format(self.lesson.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_page_order(self):
        page = Page.objects.create(lesson=self.lesson, text='text', page_number=1)
        page2 = Page.objects.create(lesson=self.lesson, text='text2', page_number=2)
        page3 = Page.objects.create(lesson=self.lesson, text='text3', page_number=3)
        response = client.post('/api/lesson/{}/order/'.format(self.lesson.id), 
                              json.dumps({ 
                                  'pages': [3, 1 ,2]
                              }), content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
