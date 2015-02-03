# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    alt_id = models.IntegerField(primary_key=True)
    alt_rep = models.ForeignKey('Report', blank=True, null=True)
    alt_prj = models.ForeignKey('Project', blank=True, null=True)
    alt_start_date = models.DateTimeField(blank=True, null=True)
    alt_end_date = models.DateTimeField(blank=True, null=True)
    alt_type = models.CharField(max_length=1, blank=True)
    alt_ticket = models.CharField(max_length=32, blank=True)



class Call(models.Model):
    cal_id = models.IntegerField(primary_key=True)
    cal_rep = models.ForeignKey('Report', blank=True, null=True)
    cal_prj = models.ForeignKey('Project', blank=True, null=True)
    cal_date = models.DateTimeField(blank=True, null=True)
    cal_direction = models.CharField(max_length=1, blank=True)
    cal_name = models.CharField(max_length=64, blank=True)



class Duty(models.Model):
    dut_id = models.IntegerField(primary_key=True)
    dut_rep = models.ForeignKey('Report', blank=True, null=True)
    dut_start_date = models.DateTimeField(blank=True, null=True)
    dut_end_date = models.DateTimeField(blank=True, null=True)
    dut_redirection = models.CharField(max_length=1, blank=True)



class Project(models.Model):
    prj_id = models.IntegerField(primary_key=True)
    prj_name = models.CharField(max_length=32, blank=True)



class Report(models.Model):
    rep_id = models.IntegerField(primary_key=True)
    rep_usr = models.ForeignKey(User, blank=True, null=True)
    rep_status = models.CharField(max_length=1, blank=True)
    rep_send_date = models.DateTimeField(blank=True, null=True)
    rep_remove_date = models.DateTimeField(blank=True, null=True)
    rep_notes = models.TextField(blank=True)
