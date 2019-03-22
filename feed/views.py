from django.shortcuts import render, redirect
from django.utils import timezone
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
        if get_request.get('q') and get_request.get('q') != 'None':
            return Offer.objects.filter(title__icontains=self.request.GET.get('q'))

        return Offer.objects.order_by('title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


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
        return render(request, 'feed/offer_creation.html', {'form': form })


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
        object_request.image = request.POST.get('image')
        object_request.user = User.objects.get(username=user.username)
        object_request.save()
        return redirect('/requests/{}'.format(object_request.id))

    elif request.method == "GET":
        form = RequestForm()
        return render(request, 'feed/request_creation.html', {'form': form})


def get_request(request, id):
    req = Request.objects.get(id=id)
    print(req.title)
    return render(request, 'feed/request_view.html', {'offer': req})