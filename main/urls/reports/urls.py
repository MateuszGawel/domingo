from django.conf.urls import patterns, url

from main.views.reports import view


urlpatterns = patterns('',
    url(r'^(?P<rep_id>\d+)/alerts/$', view.alert_tab, name='alert_tab'),
    url(r'^(?P<rep_id>\d+)/get_alerts/$', view.get_alerts_from_jira, name='get_alerts_from_jira'),
    url(r'^(?P<rep_id>\d+)/contacts/$', view.contact_tab, name='contact_tab'),
    url(r'^(?P<rep_id>\d+)/maintenances/$', view.maintenance_tab, name='maintenance_tab'),
    url(r'^(?P<rep_id>\d+)/incidents/$', view.incident_tab, name='incident_tab'),
    url(r'^create/$', view.create, name='create'),
    url(r'^(?P<rep_id>\d+)/close/$', view.close, name='close'),

    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/incident_alerts/$', view.incident_alert_tab, name='incident_alert_tab'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/incident_contacts/$', view.incident_contact_tab, name='incident_contact_tab'),
    url(r'^(?P<rep_id>\d+)/(?P<inc_id>\d+)/incident_maintenances/$', view.incident_maintenance_tab, name='incident_maintenance_tab'),

    url(r'^search/$', view.search, name='search'),

    url(r'^$', view.index, name='index'),
)