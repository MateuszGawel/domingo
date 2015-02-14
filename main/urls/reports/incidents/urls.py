from django.conf.urls import patterns, url
from main.views.reports.contacts import view


urlpatterns = patterns('',
    url(r'^(?P<inc_id>\d+)/$', view.details, name='details'),
    url(r'^(?P<inc_id>\d+)/edit/$', view.edit, name='edit'),
)