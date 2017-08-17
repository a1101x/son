import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.lesson.models import LessonSet, Lesson, Page, Favorite
from apps.userprofile.models import User


client = Client()


class FavoriteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(email='auth@gmail.com', password='passwd')
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        self.lessonset = LessonSet.objects.create(topic='lesson set topic')
        self.lesson = Lesson.objects.create(topic='lesson topic', lesson_set=self.lessonset)
        self.page = Page.objects.create(text='page text', page_number=1, lesson=self.lesson)
        self.favorite = Favorite.objects.create(user=self.user, page=self.page)
   
    def test_favorite_create(self):
        response = client.post('/api/favorite/', json.dumps({ 'user': self.user.id, 'page': self.page.id }), 
                               content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_detail(self):
        response = client.get('/api/favorite/{}/'.format(self.favorite.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favorite_list(self):
        response = client.get('/api/favorite/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favorite_delete(self):
        response = client.delete('/api/favorite/{}/'.format(self.favorite.id), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
