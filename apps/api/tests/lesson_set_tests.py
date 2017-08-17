import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet
from apps.userprofile.models import User


client = Client()


class LessonSetTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
   
    def test_lessonset_create(self):
        lessonset1 = client.post('/api/lesson_set/', json.dumps({ 'topic': 'topic1', 'description': 'desc1' }), 
                                 content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(lessonset1.status_code, status.HTTP_201_CREATED)
        lessonset2 = client.post('/api/lesson_set/', json.dumps({ 'topic': 'topic2', 'description': 'desc2' }), 
                                 content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(lessonset2.status_code, status.HTTP_201_CREATED)

    def test_lessonset_update(self):
        response = client.put('/api/lesson_set/{}/'.format(self.lessonset.id), 
                              json.dumps({ 'topic': 'topic1234', 'description': 'desc123232' }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessonset_detail(self):
        response = client.get('/api/lesson_set/{}/'.format(self.lessonset.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessonset_list(self):
        response = client.get('/api/lesson_set/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lessonset_delete(self):
        response = client.delete('/api/lesson_set/{}/'.format(self.lessonset.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    