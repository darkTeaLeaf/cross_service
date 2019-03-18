from django.test import TestCase


class LoginTests(TestCase):

    def user_creation(self):
        User.objects.create_user(username='1', password='1')
        self.assertTrue(User.objects.get(username='1') != None)
