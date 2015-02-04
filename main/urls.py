from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

urlpatterns = patterns('',
    url(r'^domingo/', views.index, name='index'),
    url(r'^login/$', views.do_login, name='do_login'),
    url(r'^logout/$', views.do_logout, name='do_logout'),
)
