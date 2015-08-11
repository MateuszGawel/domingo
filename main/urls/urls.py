from django.conf.urls import patterns, url
import main.receivers
from main.views import view


urlpatterns = patterns('',
    url(r'^logout/$', view.do_logout, name='do_logout'),
    url(r'^reset_password/(?P<username>\w+)$', view.reset_password, name='reset_password'),
    url(r'^$', view.index, name='index'),
)
