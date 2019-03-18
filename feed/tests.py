from django.test import TestCase
from django.contrib.auth.models import User


class AccountTests(TestCase):

    def test_user_creation(self):
        User.objects.create_user(username='1', password='1')
        self.assertTrue(User.objects.get(username='1') != None)

    def test_login(self):
        pass

    def test_signup(self):
        pass

    def test_account_management(self):
        pass


class OffersTests(TestCase):

    def test_offer_creation(self):
        pass

    def test_offer_view(self):
        pass


