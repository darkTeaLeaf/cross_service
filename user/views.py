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
        # form = CreateUserForm(request.POST)
        #
        # if form.is_valid():
        #     print('valid')
        #     form.save()
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password1']
        #     user = authenticate(username=username, password=password)
        #     user.save()
        #     return redirect("/user/all/?p=on&l=on")
        # print('not valid')
        # return redirect('/user/create_user/')
        print("I am here")
        print(request.POST)
        return redirect('/')
