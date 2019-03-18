from django.contrib.auth import authenticate, login
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
        username = request.POST.get('username')
        email = request.POST.get('email')
        psw = request.POST.get('psw')

        user = User.objects.create_user(username=username,
                                        email=email)

        user.set_password(request.POST.get('psw'))
        user.save()
        login(request, user)

        return redirect('/')


def user_info(request):
    # user = request.user
    # if user.is_authenticated():    
    return render(request, 'user/index.html', {})