from django.conf.urls import patterns, url

from main.views.reports.alerts import view


urlpatterns = patterns('',
    url(r'^(?P<alt_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<alt_id>\d+)/quick_edit/$', view.quick_edit, name='quick_edit'),
    url(r'^(?P<alt_id>\d+)/remove/$', view.remove, name='remove_alert'),
)