from django.conf.urls import patterns, url
from main.views.reports.alerts import view


urlpatterns = patterns('',
    url(r'^add/alert$', view.add, name='add'),
    url(r'^(?P<alt_id>\d+)/$', view.edit, name='index'),
)