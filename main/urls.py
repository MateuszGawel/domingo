from django.conf.urls import patterns, url

from main.views import main_view, report_view



urlpatterns = patterns('',
    #main
    url(r'^login/$', main_view.do_login, name='do_login'),
    url(r'^logout/$', main_view.do_logout, name='do_logout'),

    #reports
    url(r'^report/new', report_view.create_report, name='create_report'),
    url(r'^report/current', report_view.edit_report, name='edit_report'),
    url(r'^report/close', report_view.close_report, name='close_report'),
    url(r'^report/alert', report_view.add_alert, name='add_alert'),

    #default
    url(r'[a-z]*', main_view.index, name='index'),
)
