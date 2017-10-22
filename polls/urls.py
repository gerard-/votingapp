from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/cancel_vote/$', views.cancel_vote, name='cancel_vote'),
    url(r'^(?P<question_id>[0-9]+)/open/$', views.open, name='open'),
    url(r'^(?P<question_id>[0-9]+)/close/$', views.close, name='close'),
    url(r'^(?P<question_id>[0-9]+)/show/$', views.show, name='show'),
    url(r'^(?P<question_id>[0-9]+)/hide/$', views.hide, name='hide'),
    url(r'^(?P<question_id>[0-9]+)/reset/$', views.reset, name='reset'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/polls/login'}, name='logout'),

    url(r'^usergen/$', views.usergen, name='usergen'),
    url(r'^usergen/generate/$', views.usergen_generate, name='usergen_generate'),
]
