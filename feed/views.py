from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.models import User
from feed.forms import OfferForm
from feed.models import Offer


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

    if request.method == "POST":
        offer = Offer()
        offer.title = request.POST.get('title')
        offer.offer_description = request.POST.get('offer_description')
        offer.user = User.objects.get(username=request.user.username)
        offer.save()
        print(offer.offer_description)
        return render(request, 'feed/offer_view.html', {'title': offer.title, 'offer_desc': offer.offer_description})
        # return redirect('/offers/?id={}'.format(offer.id))

    elif request.method == "GET":
        form = OfferForm()
        return render(request, 'feed/offer_creation.html', {'form': form })