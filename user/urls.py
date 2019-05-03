from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.CreateUserView.as_view(), name='signup'),
    url(r'^$', views.user_info, name='user_info1'),
    url(r'^(?P<id>\d+)/$', views.user_info, name='user_info2'),
    url(r'^(?P<user_id>\d+)/feedback/request_(?P<request_id>\d+)$', views.CreateFeedbackView.as_view(), name='create_feedback'),
    url(r'^(?P<user_id>\d+)/feedback/(?P<feedback_id>\d+)$', views.get_feedback, name='get_feedback'),
    url(r'^(?P<user_id>\d+)/feedback/all', views.get_all_feedbacks, name='get_all_feedbacks'),
    url('signin/', auth_views.LoginView.as_view(template_name='user/signin.html')),
    url('signout/', views.logout_view, name='logout'),
    url(r'edit/', views.EditUserView.as_view(), name='edit'),
    url(r'^respond_request/(?P<id>\d+)$', views.accept_request_performer, name='accept_request_response'),
    url(r'^respond_offer/(?P<id>\d+)/(?P<action>[a-z]+)$', views.process_offer_respond, name='accept_offer_response'),
    url(r'^requests/(?P<id>\d+)/close/$', views.close_request, name='close_request'),
    url(r'^requests/(?P<id>\d+)/reopen/$', views.reopen_request, name='reopen_request'),
    url(r'^offers/(?P<id>\d+)/close/$', views.close_offer, name='close_offer'),
    url(r'^offers/(?P<id>\d+)/reopen/$', views.reopen_offer, name='reopen_offer'),
]   