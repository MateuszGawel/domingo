from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^reports/', include('main.urls.reports.urls', namespace="reports")),
    url(r'^reports/(?P<rep_id>\d+)/alerts/', include('main.urls.reports.alerts.urls', namespace="alerts")),
    url(r'^reports/(?P<rep_id>\d+)/contacts/', include('main.urls.reports.contacts.urls', namespace="contacts")),
    url(r'^reports/(?P<rep_id>\d+)/maintenances/', include('main.urls.reports.maintenances.urls', namespace="maintenances")),
    url(r'^reports/(?P<rep_id>\d+)/incidents/', include('main.urls.reports.incidents.urls', namespace="incidents")),

    url(r'^announcements/', include('main.urls.announcements.urls', namespace="announcements")),

    url(r'', include('main.urls.urls', namespace="main")),
)