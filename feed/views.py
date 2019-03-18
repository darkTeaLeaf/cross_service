from django.shortcuts import render
from django.views.generic import ListView
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
