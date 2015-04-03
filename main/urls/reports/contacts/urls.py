from django.conf.urls import patterns, url
from main.views.reports.contacts import view


urlpatterns = patterns('',
    url(r'^add/alert$', view.add, name='add'),
    url(r'^(?P<con_id>\d+)/$', view.edit, name='index'),
)