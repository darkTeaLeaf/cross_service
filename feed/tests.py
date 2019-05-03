from django.http import HttpRequest
from django.test import TestCase
# from .models import User
from feed.views import IndexView
from user.views import logout_view
import user.views as view
from .models import Offer
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.conf import settings
from importlib import import_module


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
        self.assertEqual(len(Offer.objects.values()), 1)

    def test_feed(self):
        p = User.objects.create_user('provider_name', 'example@mail.ru', 'pass',
                                     first_name='Elvira', last_name='Espindola')
        self.assertEqual(len(User.objects.values()), 1)

        request = HttpRequest()
        request.method = "GET"
        request.user = p
        request.GET['id'] = p.id

        index_view = IndexView.as_view()(request)
        self.assertEqual(index_view.status_code, 200)

    def test_edit(self):
        user = User.objects.create_user('s', 'exampl@mail.ru', '123456qwerty', first_name='F', last_name='L')
        user = authenticate(username='s', password='123456qwerty')
        request = HttpRequest()
        request.user = user
        request.POST['first_name'] = "newF"
        request.POST['last_name'] = "newL"
        request.POST['email'] = "newexampl@mail.ru"

        user.first_name = "newF"
        user.last_name = "newL"
        user.email = "newexampl@mail.ru"

        edit_view = view.EditUserView()
        edit_view.post(request)
        edited_user = User.objects.get(username=user.username)

        self.assertEqual(user, edited_user)

    def test_signin(self):
        user = User.objects.create_user('s', 'exampl@mail.ru', '123456qwerty', first_name='F', last_name='L')
        user = authenticate(username='s', password='123456qwerty')
        request = HttpRequest()
        request.method = "GET"
        request.user = user
        request.GET['id'] = user.id

        response = view.user_info(request)
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.POST['username'] = "sign"
        request.POST['email'] = "sign@mail.ru"
        request.POST['psw'] = "sign"

        view.CreateUserView().post(request)

        self.assertEqual(len(User.objects.values()), 1)
