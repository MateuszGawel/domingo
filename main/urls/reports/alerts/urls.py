from django.conf.urls import patterns, url
from main.views.reports.alerts import view


urlpatterns = patterns('',
    url(r'^(?P<alt_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<alt_id>\d+)/edit/$', view.edit, name='edit'),
    url(r'^(?P<alt_id>\d+)/remove/$', view.remove, name='remove_alert'),
)