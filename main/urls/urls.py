from django.conf.urls import patterns, url
from main.views import view


urlpatterns = patterns('',
    url(r'^login/$', view.do_login, name='do_login'),
    url(r'^logout/$', view.do_logout, name='do_logout'),

    url(r'^$', view.index, name='index'),
)
