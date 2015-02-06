from django.conf.urls import patterns, url

from main.views import main_view, report_view



urlpatterns = patterns('',
    #main
    url(r'^domingo/', main_view.index, name='index'),
    url(r'^login/$', main_view.do_login, name='do_login'),
    url(r'^logout/$', main_view.do_logout, name='do_logout'),

    #reports
    url(r'^report/current$', report_view.start_duty, name='start_duty'),
    url(r'^report/alert$', report_view.add_alert, name='add_alert'),

)
