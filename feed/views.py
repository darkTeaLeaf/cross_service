from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.models import User
from feed.forms import OfferForm, RequestForm
from feed.models import Offer, Request


class IndexView(ListView):
    """
    main page for browsing documents
    """
    template_name = 'feed/index.html'
    model = Offer
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        get_request = self.request.GET

        # quick search
        search_tag = get_request.get('search_tag')
        if get_request.get('q') and get_request.get('q') != 'None':
            if search_tag == 'title':
                return self.model.objects.filter(title__icontains=self.request.GET.get('q'))
            elif search_tag == 'user':
                return self.model.objects.filter(user__username=self.request.GET.get('q'))
        return self.model.objects.order_by('title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class IndexRequestsView(IndexView):
    model = Request
    context_object_name = 'requests'


def get_offer_creation(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/user/signin/')

    if request.method == "POST":
        offer = Offer()
        offer.title = request.POST.get('title')
        offer.offer_description = request.POST.get('offer_description')
        offer.user = User.objects.get(username=user.username)
        offer.save()
        return redirect('/offers/{}'.format(offer.id))

    elif request.method == "GET":
        form = OfferForm()
        return render(request, 'feed/offer_creation.html', {'form': form})


def get_offer(request, id):
    of = Offer.objects.get(id=id)
    print(of.title)
    return render(request, 'feed/offer_view.html', {'offer': of})


def get_request_creation(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/user/signin/')

    if request.method == "POST":
        object_request = Request()
        object_request.title = request.POST.get('title')
        object_request.service_type = request.POST.get('service_type')
        object_request.price = request.POST.get('price')
        object_request.start_date = request.POST.get('start_date')
        object_request.deadline = request.POST.get('deadline')
        object_request.request_description = request.POST.get('offer_description')

        image = request.FILES.get('image', False)
        object_request.image = image

        object_request.user = User.objects.get(username=user.username)
        object_request.save()
        return redirect('/requests/{}'.format(object_request.id))

    elif request.method == "GET":
        form = RequestForm()
        return render(request, 'feed/request_creation.html', {'form': form})


def get_request(request, id):
    req = Request.objects.get(id=id)
    return render(request, 'feed/request_view.html', {'req': req})


def edit_request(request, id):
    if request.method == "POST":

        object_request = Request.objects.get(id=id)
        object_request.title = request.POST.get('title')
        object_request.service_type = request.POST.get('service_type')
        object_request.price = request.POST.get('price')
        object_request.start_date = request.POST.get('start_date')
        object_request.deadline = request.POST.get('deadline')
        object_request.request_description = request.POST.get('offer_description')

        image = request.FILES.get('image', False)
        object_request.image = image

        object_request.save()
        return redirect('/requests/{}'.format(object_request.id))

    elif request.method == "GET":
        req = Request.objects.get(id=id)
        return render(request, 'feed/request_edit.html', {'req': req})
