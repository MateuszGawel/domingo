from django.conf.urls import patterns, url

from main.views.reports import view


urlpatterns = patterns('',
    url(r'^(?P<rep_id>\d+)/$', view.summary_tab, name='summary_tab'),
    url(r'^(?P<rep_id>\d+)/alerts/$', view.alert_tab, name='alert_tab'),
    url(r'^(?P<rep_id>\d+)/contacts/$', view.contact_tab, name='contact_tab'),
    url(r'^(?P<rep_id>\d+)/maintenances/$', view.maintenance_tab, name='maintenance_tab'),
    url(r'^(?P<rep_id>\d+)/incidents/$', view.incident_tab, name='incident_tab'),


    url(r'^(?P<rep_id>\d+)/incidents/(?P<inc_id>\d+)/alerts/$', view.incident_alert_tab, name='incident_alert_tab'),
    url(r'^(?P<rep_id>\d+)/incidents/(?P<inc_id>\d+)/contacts/$', view.incident_contact_tab, name='incident_contact_tab'),
    url(r'^(?P<rep_id>\d+)/incidents/(?P<inc_id>\d+)/maintenances/$', view.incident_maintenance_tab, name='incident_maintenance_tab'),



    url(r'^create/$', view.create, name='create'),
    url(r'^(?P<rep_id>\d+)/close/$', view.close, name='close'),
    url(r'^(?P<rep_id>\d+)/get_alerts/$', view.get_alerts_from_jira, name='get_alerts_from_jira'),

    url(r'^search/$', view.search, name='search'),

    url(r'^$', view.index, name='index'),
)