from django.test import TestCase

from apps.userprofile.models import User


class UserTestCase(TestCase):
    
    def setUp(self):
        User.objects.create(email='test1@gmail.com')
        User.objects.create(email='test2@gmail.com', is_blocked=True)

    def test_email(self):
        test1 = User.objects.get(email='test1@gmail.com')
        test2 = User.objects.get(email='test2@gmail.com')
        self.assertEqual(test1.email, 'test1@gmail.com')
        self.assertNotEqual(test1.email, 'abracadabra@gmail.com')
        self.assertEqual(test2.email, 'test2@gmail.com')
    
    def test_is_blocked(self):
        test1 = User.objects.get(email='test1@gmail.com')
        test2 = User.objects.get(email='test2@gmail.com')
        self.assertFalse(test1.is_blocked)
        self.assertTrue(test2.is_blocked)
