from django.conf.urls import patterns, url

from main.views.announcements import view


urlpatterns = patterns('',
    url(r'^$', view.index, name='index'),
)