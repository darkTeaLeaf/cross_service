from django import template

from feed.models import RespondRequest

register = template.Library()


@register.filter
def get_respond(request):
    respond_requests = RespondRequest.objects.filter(request_id=request)
    return respond_requests
