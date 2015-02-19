from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reports/', include('main.urls.reports.urls', namespace="reports")),
    url(r'^reports/alerts/', include('main.urls.reports.alerts.urls', namespace="alerts")),
    url(r'^reports/contacts/', include('main.urls.reports.contacts.urls', namespace="contacts")),
    url(r'^reports/maintenances/', include('main.urls.reports.maintenances.urls', namespace="maintenances")),
    url(r'^reports/incidents/', include('main.urls.reports.incidents.urls', namespace="incidents")),
    url(r'', include('main.urls.urls', namespace="main")),
)