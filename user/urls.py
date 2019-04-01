from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.CreateUserView.as_view(), name='signup'),
    url(r'^$', views.user_info, name='user_info1'),
    url(r'^(?P<id>\d+)/$', views.user_info, name='user_info2'),
    url(r'^(?P<user_id>\d+)/feedback', views.create_feedback, name='create_feedback'),
    url(r'^(?P<user_id>\d+)/feedback(?P<feedback_id>\d+)$', views.get_feedback, name='get_feedback'),
    url('signin/', auth_views.LoginView.as_view(template_name='user/signin.html')),
    url('signout/', views.logout_view, name='logout'),
    url(r'edit/', views.EditUserView.as_view(), name='edit')
]