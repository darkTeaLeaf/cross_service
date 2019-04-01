from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import *
from .models import *
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.contrib import messages
from re import match


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
        UserProfile.objects.create(user=user, alias=request.POST.get('alias'))
        user.save()
        login(request, user)
        return redirect('/')


class EditUserView(View):

    def get(self, request):
        return render(request, 'user/edit.html', {})

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.userprofile.bio = request.POST.get('bio')
        user.userprofile.alias = request.POST.get('alias')
        user.userprofile.save()
        oldpsw = request.POST.get('oldpsw', '')
        if oldpsw and check_password(oldpsw, user.password):
            user.set_password(request.POST.get('newpsw'))
            login(request, user)
        # TODO else НУЖНО КАК-ТО ЧТО-ТО ВЫВЕСТИ. Мол неправильный пароль
        # Да и на успех лучше не редиректить сразу, а выдать что-то вроде "УСПЕХ, УМНИЦА"
        user.save()

        return redirect('/user/')

        
def leave_feedback(request, user_id):
    if request.method == "POST":
        if str(request.user.id) == user_id: 
            messages.error(request, 'You cannot leave feedback for yourself')
            return redirect('/user/'+user_id+'/feedback')
        else:
            feedback = Feedback()
            feedback.userFrom = request.user
            feedback.userTo = User.objects.get(id=user_id)
            feedback.feedback_text = request.POST.get('inputFeedback')
            feedback.grade = request.POST.get('rating')
            feedback.save()
            
            messages.success(request, 'Your feedback is saved!')
            return redirect('/user/'+user_id+'/feedback/{}'.format(feedback.id))

    elif request.method == "GET":
        target = User.objects.get(id=user_id)
        return render(request, 'user/feedback.html', {'target': target})


def user_info(request, id=0):

    if id == 0:  # my page
        user = request.user
        # return render(request, 'user/index.html', {''})
    else:  # page of another user
        user = User.objects.get(id=id)
    return render(request, 'user/index.html', {'client': user, 'me': user.id==request.user.id})


def logout_view(request):
    logout(request)
    return redirect('/user/signin')
