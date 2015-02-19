from django.conf.urls import patterns, url

from main.views.reports.incidents import view


urlpatterns = patterns('',
    url(r'^(?P<inc_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<inc_id>\d+)/edit/$', view.edit, name='edit'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/invalidate/$', view.invalidate, name='invalidate'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/close/$', view.close, name='close'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/reopen/$', view.reopen, name='reopen'),

    url(r'^(?P<inc_id>\d+)/join_alert/$', view.join_alert, name='join_alert'),
    url(r'^(?P<inc_id>\d+)/join_contact/$', view.join_contact, name='join_contact'),
    url(r'^(?P<inc_id>\d+)/join_maintenance/$', view.join_maintenance, name='join_maintenance'),

    url(r'^(?P<ins_id>\d+)/remove_incident_step/$', view.remove_incident_step, name='remove_incident_step'),
)