from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reports/', include('main.urls.reports.urls', namespace="reports")),
    url(r'^reports/alerts/', include('main.urls.reports.alerts.urls', namespace="alerts")),
    url(r'^reports/contacts/', include('main.urls.reports.contacts.urls', namespace="contacts")),
    url(r'', include('main.urls.urls', namespace="main")),
)