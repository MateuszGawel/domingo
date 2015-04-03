from django.conf.urls import patterns, url
from main.views.reports import view


urlpatterns = patterns('',
    url(r'^current/$', view.edit, name='edit'),
    url(r'^current/create/$', view.create, name='create'),
    url(r'^current/close/$', view.close, name='close'),

    url(r'^search/$', view.search, name='search'),

    url(r'^$', view.index, name='index'),
)