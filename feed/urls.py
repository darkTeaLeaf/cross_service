from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='signup'),
    url(r'^offer_creation/$', views.get_offer_creation, name='offer_creation'),
]
