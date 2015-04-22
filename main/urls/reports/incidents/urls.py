from django.conf.urls import patterns, url
from main.views.reports.incidents import view


urlpatterns = patterns('',
    url(r'^(?P<inc_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<inc_id>\d+)/edit/$', view.edit, name='edit'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/invalidate/$', view.invalidate, name='invalidate'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/close/$', view.close, name='close'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/reopen/$', view.reopen, name='reopen'),
)