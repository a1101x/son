import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils

from apps.api.serializers.userprofile import UserSerializer
from apps.userprofile.models import User


client = Client()


class UserTest(TestCase):

    def setUp(self):
        self.email = 'auth@gmail.com'
        self.password = 'passwd'
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_superuser(email=self.email, password=self.password)
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {}'.format(token)
        User.objects.create_user(email='test1@gmail.com', password='password')
        User.objects.create(email='test2@gmail.com', is_blocked=True)

    def test_all_users(self):
        response = client.get('/api/user/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_user_detail(self):
        user_id_1 = User.objects.get(email='test1@gmail.com').id
        user_id_2 = User.objects.get(email='test2@gmail.com', is_blocked=True).id
        response = client.get('/api/user/{}/'.format(user_id_1), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/api/user/{}/'.format(user_id_2), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        user = User.objects.get(email='test1@gmail.com', is_blocked=False)
        response = client.put('/api/user/{}/'.format(user.id), json.dumps({ 'is_blocked': True }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update(self):
        admin = User.objects.get(email=self.email)
        response = client.put('/api/user/{}/'.format(admin.id), json.dumps({ 'is_blocked': True }), 
                              content_type='application/json', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
