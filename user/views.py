from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404

from feed.models import RespondRequest, Request
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


def create_feedback(request, user_id):
    if request.method == "POST":
        if str(request.user.id) == user_id:
            messages.error(request, 'You cannot leave feedback for yourself')
            return redirect('/user/' + user_id + '/feedback')
        else:
            feedback = Feedback()
            feedback.userFrom = request.user
            feedback.userTo = User.objects.get(id=user_id)
            feedback.feedback_text = request.POST.get('inputFeedback')
            feedback.grade = request.POST.get('rating')
            feedback.save()

            return redirect('/user/{}/feedback/{}'.format(feedback.userTo.id, feedback.id))

    elif request.method == "GET":
        target = User.objects.get(id=user_id)
        return render(request, 'user/feedback_creation.html', {'target': target})


def get_feedback(request, user_id, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    author = feedback.userFrom
    target = User.objects.get(id=user_id)
    # TODO what if there is no such feedback ??
    return render(request, 'user/feedback_view.html', {'author': author, 'feedback': feedback, 'target': target})

def get_all_feedbacks(request, user_id=0):
    if id == 0:  # my page
        user = request.user
    else:  # page of another user
        user = User.objects.get(id=id)

    feedbacks = Feedback.objects.filter(userTo=user).order_by('-published_date')
    as_provider = Feedback.objects.filter(userTo=user, for_requester=False)
    as_requestor = Feedback.objects.filter(userTo=user, for_requester=True)

    mean = 0.0

    for feedback in feedbacks:
        mean += float(feedback.grade)
    if mean: 
        mean = round(mean/len(feedbacks))

    return render(request, 'user/feedback_page.html', {'client': user,
         'mean_feedback': int(mean), 'as_provider': as_provider, 'as_requestor': as_requestor})


def user_info(request, id=0):
    if id == 0:  # my page
        user = request.user
    else:  # page of another user
        user = User.objects.get(id=id)

    feedbacks = Feedback.objects.filter(userTo=user).order_by('-published_date')
    requests = user.request_set.order_by('-published_date')
    requests = requests.filter(visible=True)
    accepted_requests = user.request_set.order_by('-published_date')
    accepted_requests = accepted_requests.filter(visible=False)
    requests_to_do = Request.objects.filter(performer=user)
    offers = user.offer_set.order_by('-published_date')

    mean = 0.0
    for feedback in feedbacks:
        mean += float(feedback.grade)
    if mean:
        mean = round(mean / len(feedbacks))

    return render(request, 'user/index.html', {'client': user, 'me': user.id == request.user.id,
                                               'mean_feedback': int(mean), 'feedbacks': feedbacks,
                                               'accepted_requests': accepted_requests, 'requests_to_do': requests_to_do,
                                               'requests': requests, 'offers': offers})


def logout_view(request):
    logout(request)
    return redirect('/user/signin')


def accept_request_performer(request, id):
    respond = RespondRequest.objects.get(id=id)
    object_request = Request.objects.get(id=respond.request_id.id)
    object_request.performer = respond.user
    object_request.visible = False

    responds = RespondRequest.objects.filter(request_id=respond.request_id)
    responds.delete()

    object_request.save()
    return redirect('/user/{}'.format(request.user.id))
