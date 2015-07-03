from django.conf.urls import patterns, url

import main.views.reports.alerts.view
import main.views.reports.contacts.view
import main.views.reports.maintenances.view
import main.views.reports.incidents.view

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
    url(r'^search/alerts$', main.views.reports.alerts.view.search, name='alert_search'),
    url(r'^search/contacts$', main.views.reports.contacts.view.search, name='contact_search'),
    url(r'^search/maintenances$', main.views.reports.maintenances.view.search, name='maintenance_search'),
    url(r'^search/incidents$', main.views.reports.incidents.view.search, name='incident_search'),

    url(r'^$', view.index, name='index'),
)