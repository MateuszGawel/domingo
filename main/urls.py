from django.conf.urls import patterns, url

from main.views import main_view, report_view


urlpatterns = patterns('',
    #main
    url(r'^login/$', main_view.do_login, name='do_login'),
    url(r'^logout/$', main_view.do_logout, name='do_logout'),

    #reports
    url(r'^reports/$', report_view.reports, name='reports'),

    url(r'^reports/current/$', report_view.edit_report, name='edit_report'),
    url(r'^reports/current/create/$', report_view.create_report, name='create_report'),
    url(r'^reports/current/close/$', report_view.close_report, name='close_report'),
    url(r'^reports/current/add/alert$', report_view.add_alert, name='add_alert'),
    url(r'^reports/current/add/contact', report_view.add_contact, name='add_contact'),

    url(r'^reports/details/alert/(?P<alt_id>\d+)/$', report_view.edit_alert, name='alert_details'),

    url(r'^reports/browse/$', report_view.browse_reports, name='browse_reports'),
    url(r'^reports/browse/my/$', report_view.browse_my_reports, name='browse_my_reports'),
    url(r'^reports/browse/filter_results/$', report_view.filter_reports, name='filter_reports'),


    #default
    url(r'^$', main_view.index, name='index'),
)
