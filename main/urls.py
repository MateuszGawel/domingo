from django.conf.urls import patterns, url

from main.views import main_view, report_view



urlpatterns = patterns('',
    #main
    url(r'^login/$', main_view.do_login, name='do_login'),
    url(r'^logout/$', main_view.do_logout, name='do_logout'),

    #reports
    url(r'^report/current', report_view.add_alert, name='add_alert'),

    #default
    url(r'[a-z]*', main_view.index, name='index'),
)
