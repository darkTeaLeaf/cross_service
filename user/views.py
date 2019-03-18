from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import *
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


class CreateUserView(View):
    """
    user creation view
    """
    template_name = "user/signup.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        print(request.POST)
        print(request.POST.get('username'))

        user = User.objects.create_user(username=request.POST.get('username'),
                                        email=request.POST.get('email'))

        user.set_password(request.POST.get('psw'))
        user.save()
        login(request, user)
        return redirect('/')


def user_info(request, id=0):
    if id == 0:
        user = request.user
    else:
        user = User.objects.get(id=id)
    return render(request, 'user/index.html', {'client': user})

    def post(self, request):
        user = request.user
        print(user.username)

        # if check_password(request.POST.get('oldpsw'), user.password): 
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        # user.telegram_alias = request.POST.get('telegram_alias')
        # user.set_password(request.POST.get('newpsw'))
        # TODO else НУЖНО КАК-ТО ЧТО-ТО ВЫВЕСТИ. Мол неправильный пароль
        # Да и на успех лучше не редиректить сразу, а выдать что-то вроде "УСПЕХ, УМНИЦА"
        user.save()

        return redirect('/user/')

def user_info(request):
        return render(request, 'user/index.html', {})
def logout_view(request):
    logout(request)
    return redirect('/user/signin')
