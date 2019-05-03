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
from feed import permissions


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

    @permissions.required('authenticated')
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
        user.save()

        return redirect('/user/')


@permissions.required('authenticated')
def create_feedback(request, user_id, request_id):
    if request.method == "POST":
        request_adv = Request.objects.get(id=request_id)

        userTo = User.objects.get(id=user_id)
        
        for_requester = (userTo == request_adv.user) 

        try:
            Feedback.objects.get(userFrom=request.user, request=request_adv)
            messages.error(request, 'You have already left feedback for this deal')
            return redirect('/user/'+str(user_id)+'/feedback/request_'+str(request_id))

        except: 
        
            if not for_requester:
                if userTo != request_adv.performer: 
                    messages.error(request, 'This user is not a requester/performer\n You cannot leave feedback for this deal')
                    return redirect('/user/'+str(user_id)+'/feedback/request_'+str(request_id))

            if request.user == userTo:
                messages.error(request, 'You cannot leave feedback for yourself')
                return redirect('/user/'+str(user_id)+'/feedback/request_'+str(request_id))

            if request.user != request_adv.user and request.user != request_adv.performer: 
                messages.error(request, 'You are not a requester/performer\n You cannot leave feedback for this deal')
                return redirect('/user/'+str(user_id)+'/feedback/request_'+str(request_id))
                
            feedback = Feedback()
            feedback.userFrom = request.user
            feedback.userTo = User.objects.get(id=user_id)
            feedback.feedback_text = request.POST.get('inputFeedback')
            feedback.grade = request.POST.get('rating')
            feedback.for_requester = for_requester
            feedback.request = request_adv
            feedback.save()

            try:
                Feedback.objects.get(userFrom=request.user, request=request_adv)
                Feedback.objects.get(userFrom=userTo, request=request_adv)
                request_adv.closed = True
                request_adv.save()
            except:
                pass

            userTo.userprofile.recalculate_mean_grade()
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
    if user_id == 0:  # my page
        user = request.user
    else:  # page of another user
        user = User.objects.get(id=user_id)

    feedbacks = Feedback.objects.filter(userTo=user).order_by('-published_date')
    as_provider = Feedback.objects.filter(userTo=user, for_requester=False)
    as_requester = Feedback.objects.filter(userTo=user, for_requester=True)

    mean = 0.0

    for feedback in feedbacks:
        mean += float(feedback.grade)
    if mean: 
        mean = round(mean/len(feedbacks))

    return render(request, 'user/feedback_page.html', {'client': user,
         'mean_feedback': int(mean), 'as_provider': as_provider, 'as_requester': as_requester})


def user_info(request, id=0):
    if id == 0:  # my page
        user = request.user
    else:  # page of another user
        user = User.objects.get(id=id)

    feedbacks = Feedback.objects.filter(userTo=user).order_by('-published_date')
    requests = user.request_set.order_by('-published_date')
    requests = requests.filter(visible=True, closed=False)
    accepted_requests = user.request_set.order_by('-published_date')
    accepted_requests = accepted_requests.filter(visible=False, closed=False)
    requests_to_do = Request.objects.filter(performer=user, closed=False)
    closed_requests = user.request_set.filter(closed=True)
    offers = user.offer_set.order_by('-published_date')

    return render(request, 'user/index.html', {'client': user, 'me': user.id == request.user.id,
                                               'feedbacks': feedbacks,
                                               'accepted_requests': accepted_requests, 'requests_to_do': requests_to_do,
                                               'closed_requests': closed_requests,
                                               'requests': requests, 'offers': offers})


@permissions.required('authenticated')
def logout_view(request):
    logout(request)
    return redirect('/user/signin')


@permissions.required('authenticated')
def accept_request_performer(request, id):
    respond = RespondRequest.objects.get(id=id)
    object_request = Request.objects.get(id=respond.request_id.id)
    object_request.performer = respond.user
    object_request.visible = False

    responds = RespondRequest.objects.filter(request_id=respond.request_id)
    responds.delete()

    object_request.save()
    return redirect('/user/{}'.format(request.user.id))


@permissions.required('authenticated')
def close_request(request, id):
    object_request = Request.objects.get(id=id)
    object_request.closed = True

    responds = RespondRequest.objects.filter(request_id=id)
    responds.delete()

    object_request.save()
    return redirect('/user/{}'.format(request.user.id))
