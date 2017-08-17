import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, Page
from apps.userprofile.models import User


client = Client()
    

class PageTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.page = Page.objects.create(text='page text', page_number=1, lesson=self.lesson)
   
    def test_page_create(self):
        page1 = client.post('/api/page/', json.dumps({ 'text': 'text1', 'page_number': 1, 'lesson': self.lesson.id }), 
                            content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(page1.status_code, status.HTTP_201_CREATED)
        page2 = client.post('/api/page/', json.dumps({ 'text': 'text2', 'page_number': 2, 'lesson': self.lesson.id }), 
                            content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(page2.status_code, status.HTTP_201_CREATED)

    def test_page_update(self):
        lesson2 = Lesson.objects.create(topic='another lesson set topic', lesson_set=self.lessonset)
        response = client.put('/api/page/{}/'.format(self.lesson.id), 
                              json.dumps({ 
                                  'text': 'text1234', 
                                  'page_number': 999, 
                                  'lesson': lesson2.id 
                              }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_detail(self):
        response = client.get('/api/page/{}/'.format(self.page.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_list(self):
        response = client.get('/api/page/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_delete(self):
        response = client.delete('/api/page/{}/'.format(self.page.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
