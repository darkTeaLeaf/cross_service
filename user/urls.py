from django.conf.urls import url
from . import views
# from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^signup/$', views.CreateUserView.as_view(), name='signup'),
    url(r'^$', views.user_info, name='user_card_info'),
    # url(r'^signin/$', views.CreateUserView.as_view(template_name='user/signin.html'), name='login'),
    path('user/', include('django.contrib.auth.urls')),
]
