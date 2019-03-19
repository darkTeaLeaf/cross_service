from django.test import TestCase
# from .models import User
from .models import Offer
from datetime import datetime
from django.contrib.auth.models import User


class TestOffer(TestCase):

    def test_offer(self):
        p = User.objects.create_user('provider_name', 'example@mail.ru', 'pass',
                                     first_name='Elvira', last_name='Espindola')
        self.assertEqual(len(User.objects.values()), 1)

        o = Offer()
        o.offer_description = "Dummy description"
        o.title = "Dummy title"
        o.user = User.objects.get(username=p.username)
        o.save()
        # print("Offers ", Offer.objects.values())
        self.assertEqual(len(Offer.objects.values()), 1)