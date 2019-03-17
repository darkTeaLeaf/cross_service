from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import *
from django.db.models import Q
from django.views.generic import View, ListView


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
        return redirect('/user/signup/')


def user_info(request):
    return render(request, 'user/index.html', {})
