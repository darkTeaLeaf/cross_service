from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import *
from django.db.models import Q
from django.views.generic import View, ListView
import datetime


class CreateUserView(View):
    """
    user creation view
    """
    template_name = "user/signup.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        user = User.objects.create_user(username=request.POST.get('username'),
                                        email=request.POST.get('email'))

        user.set_password(request.POST.get('password'))
        print(request.POST)
        return redirect('/user/signup/')
