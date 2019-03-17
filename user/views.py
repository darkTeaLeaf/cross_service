from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from django.views.generic import View, ListView
import datetime


class CreateUserView(View):
    """
    user creation view
    """
    template_name = "user/signup.html"

    def get(self, request):
        # form = AdminCreateUserForm() if \
        #         request.user.is_superuser else CreateUserForm()
        return render(request, self.template_name, {})

    # def post(self, request):
    #         if request.user.is_superuser or (not request.POST['privileges'].startswith('priv') and
    #                                                                                         request.user.is_staff):
    #             form = AdminCreateUserForm(request.POST) if \
    #                 request.user.is_superuser else CreateUserForm(request.POST)
    #
    #             if form.is_valid():
    #                 print('valid')
    #                 form.save()
    #                 if form.cleaned_data['status'] == 'admin':
    #                     raise Http404('Permission denied')
    #                 username = form.cleaned_data['username']
    #                 password = form.cleaned_data['password1']
    #                 user = authenticate(username=username, password=password)
    #                 user.save()
    #                 logging.info('{} created user {}({}) by: {}({});'.format(str(datetime.date.today()), user.username, user.userprofile.status,
    #                                                                       request.user.username,
    #                                                                       request.user.userprofile.status))
    #                 return redirect("/user/all/?p=on&l=on")
    #             print('not valid')
    #             return redirect('/user/create_user/')
    #         else:
    #             return redirect('/user/create_user/')
