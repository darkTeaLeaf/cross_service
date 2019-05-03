from django import template

from feed.models import RespondRequest, RespondOffer

register = template.Library()


@register.filter
def get_request_respond(request):
    respond_requests = RespondRequest.objects.filter(request_id=request)
    return respond_requests

@register.filter
def get_offer_respond(offer):
    respond_offers = RespondOffer.objects.filter(offer=offer)
    return respond_offers