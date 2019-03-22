from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='signup'),
    url(r'^offer_creation/$', views.get_offer_creation, name='offer_creation'),
    url(r'^offers/(?P<id>\d+)$', views.get_offer, name='get_offer'),
    url(r'^request_creation/$', views.get_request_creation, name='request_creation'),
    url(r'^requests/(?P<id>\d+)$', views.get_request, name='get_request'),
]
