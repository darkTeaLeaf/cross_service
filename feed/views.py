from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from feed.forms import OfferForm, RequestForm
from feed.models import Offer, Request, RespondRequest, RespondOffer
from . import permissions


class IndexView(ListView):
    """
    main page for browsing documents
    """
    template_name = 'feed/index.html'
    model = Offer
    context_object_name = 'offers'
    paginate_by = 9

    def get_queryset(self):
        """
        :returns: the set of documents that will be displayed on the main page
        """
        get_request = self.request.GET

        # quick search
        search_tag = get_request.get('optradio')
        if get_request.get('q') and get_request.get('q') != 'None':
            if search_tag == 'bytitle':
                result = self.model.objects.filter(title__icontains=self.request.GET.get('q'))
            elif search_tag == 'byauthor':
                result = self.model.objects.filter(user__username__icontains=self.request.GET.get('q'))
            elif search_tag == 'bymonth' and 0 < int(self.request.GET.get('q')) < 13:
                result = self.model.objects.filter(published_date__month=self.request.GET.get('q'))
        else:
            result = self.model.objects.order_by('title')
        if self.model == Request:
            result = result.filter(visible=True)
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['optradio'] = self.request.GET.get('optradio', '')
        return context


class IndexRequestsView(IndexView):
    model = Request
    context_object_name = 'requests'


@permissions.required('authenticated')
def get_offer_creation(request):
    user = request.user

    if request.method == "POST":
        offer = Offer()
        offer.title = request.POST.get('title')
        offer.service_type = request.POST.get('service_type')
        offer.price = request.POST.get('price')
        offer.start_date = request.POST.get('start_date')
        offer.deadline = request.POST.get('deadline')
        offer.offer_description = request.POST.get('offer_description')

        image = request.FILES.get('image', False)
        offer.image = image

        offer.user = User.objects.get(username=user.username)
        offer.save()
        return redirect('/offers/{}'.format(offer.id))

    elif request.method == "GET":
        form = OfferForm()
        return render(request, 'feed/offer_creation.html', {'form': form})


class OfferView(DetailView):
    model = Offer
    template_name = 'feed/offer_view.html'


@permissions.required('authenticated')
def edit_offer(request, id):

    offer = Offer.objects.get(id=id)
    if not request.user.is_superuser and not request.user.id == offer.user.id:
        redirect('/')
    if request.method == "POST":

        offer.title = request.POST.get('title')
        offer.service_type = request.POST.get('service_type')
        offer.price = request.POST.get('price')
        offer.start_date = request.POST.get('start_date')
        offer.deadline = request.POST.get('deadline')
        offer.offer_description = request.POST.get('offer_description')

        image = request.FILES.get('image', offer.image)
        offer.image = image

        offer.save()
        return redirect('/offers/{}'.format(offer.id))

    elif request.method == "GET":
        return render(request, 'feed/offer_edit.html', {'offer': offer})

def request_creation(request, user, visible):
    object_request = Request()
    object_request.visible = visible
    object_request.closed = False
    object_request.title = request.POST.get('title')
    object_request.service_type = request.POST.get('service_type')
    object_request.price = request.POST.get('price')
    object_request.start_date = request.POST.get('start_date')
    object_request.deadline = request.POST.get('deadline')
    object_request.request_description = request.POST.get('request_description')

    image = request.FILES.get('image', False)
    object_request.image = image

    object_request.user = User.objects.get(username=user.username)
    object_request.save()
    
    return object_request

@permissions.required('authenticated')
def get_request_creation(request):
    user = request.user

    if request.method == "POST":
        object_request = request_creation(request, user, True)
        
        return redirect('/requests/{}'.format(object_request.id))

    elif request.method == "GET":

        return render(request, 'feed/request_creation.html')


class RequestView(DetailView):
    model = Request
    template_name = 'feed/request_view.html'
    context_object_name = 'req'


@permissions.required('authenticated')
def edit_request(request, id):
    if request.method == "POST":

        object_request = Request.objects.get(id=id)
        object_request.title = request.POST.get('title')
        object_request.service_type = request.POST.get('service_type')
        object_request.price = request.POST.get('price')
        object_request.start_date = request.POST.get('start_date')
        object_request.deadline = request.POST.get('deadline')
        object_request.request_description = request.POST.get('request_description')

        image = request.FILES.get('image', object_request.image)
        object_request.image = image

        object_request.save()
        return redirect('/requests/{}'.format(object_request.id))

    elif request.method == "GET":
        req = Request.objects.get(id=id)
        return render(request, 'feed/request_edit.html', {'req': req})


@permissions.required('authenticated')
def create_respond_request(request, id):
    user = request.user

    if request.method == "POST":
        respond_request = RespondRequest()
        respond_request.request_id = Request.objects.get(id=id)
        respond_request.user = User.objects.get(username=user.username)
        respond_request.message = request.POST.get('message')

        respond_request.save()
        return render_to_response('feed/success_page.html')

    elif request.method == "GET":

        return render(request, 'feed/respond_request.html')


@permissions.required('authenticated')
def create_respond_offer(request, id):
    user = request.user

    if request.method == "POST":
        respond_offer = RespondOffer()
        respond_offer.offer = Offer.objects.get(id=id)
        respond_offer.request_as_response = request_creation(request, user, False)
        
        respond_offer.save()

        return redirect('/requests/{}'.format(respond_offer.request_as_response.id))

    elif request.method == "GET":
        return render(request, 'feed/request_creation.html')


def handler404(request, *args, **kwargs):
    pass


def handler500(request, *args, **kwargs):
    pass
