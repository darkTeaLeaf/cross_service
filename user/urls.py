from django.conf.urls import url
from . import views
# from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^signup/$', views.CreateUserView.as_view(), name='signup'),
]
