from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.CreateUserView.as_view(), name='signup'),
    url(r'^$', views.user_info, name='user_card_info'),
    url('signin/', auth_views.LoginView.as_view(template_name='user/signin.html')),
    # url('signout/', auth_views.LoginView.as_view(template_name='user/signin.html')),
    url('signout/', views.logout_view, name='logout'),
    # path('user/', include('django.contrib.auth.urls')),
]
