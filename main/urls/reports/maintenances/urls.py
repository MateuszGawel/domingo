from django.conf.urls import patterns, url

from main.views.reports.maintenances import view


urlpatterns = patterns('',
    url(r'^(?P<mnt_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<mnt_id>\d+)/quick_edit/$', view.quick_edit, name='quick_edit'),
    url(r'^(?P<mnt_id>\d+)/remove/$', view.remove, name='remove_maintenance'),
)