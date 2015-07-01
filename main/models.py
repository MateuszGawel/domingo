from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    REPORT_STATUSES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )

    rep_id = models.AutoField(primary_key=True, verbose_name="Report ID")
    rep_status = models.CharField(max_length=1, blank=True, choices=REPORT_STATUSES, verbose_name="Report status")
    rep_date_created = models.DateTimeField(blank=True, null=True, verbose_name="Report creation date")
    rep_date_sent = models.DateTimeField(blank=True, null=True, verbose_name="Report sent date")
    rep_redirection = models.DateTimeField(blank=True, null=True, verbose_name="Report redirection check")
    rep_usr_id = models.ForeignKey(User, blank=True, null=True, verbose_name="Report user FK")
    rep_com_id = models.ForeignKey("Comment", blank=True, null=True, verbose_name="Report comment FK")

    def __unicode__(self):
        return str( self.rep_id )


class Comment(models.Model):
    com_id = models.AutoField(primary_key=True, verbose_name="Comment ID")
    com_value = models.TextField(blank=True, verbose_name="Comment content")

    def __unicode__(self):
        return str( self.com_id )


class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, verbose_name="Project ID")
    prj_name = models.CharField(max_length=64, blank=True, verbose_name="Project full name")

    def __unicode__(self):
        return str( self.prj_name )


class Incident(models.Model):
    INCIDENT_STATUSES = (
        ('O', 'Open'),
        ('R', 'Resolved'),
        ('I', 'Invalid'),
    )
    inc_id = models.AutoField(primary_key=True, verbose_name="Incident ID")
    inc_date_start = models.DateTimeField(blank=True, null=True, verbose_name="Incident start date")
    inc_date_end = models.DateTimeField(blank=True, null=True, verbose_name="Incident end date")
    inc_status = models.CharField(max_length=1, blank=True, choices=INCIDENT_STATUSES, verbose_name="Incident status")
    inc_ticket = models.CharField(max_length=100, blank=True, verbose_name="Incident ticket link")
    inc_prj_id = models.ForeignKey('Project', blank=True, null=True, verbose_name="Incident project FK")
    inc_rca = models.BooleanField(blank=True, default="False", verbose_name="Incident RCA")
    inc_com_id = models.ForeignKey("Comment", blank=True, null=True, verbose_name="Incident comment FK")


    def __unicode__(self):
        return str( self.inc_id )


class IncidentStep(models.Model):
    INCIDENT_STEP_TYPE = (
        ('C', 'Contact'),
        ('A', 'Alert'),
        ('M', 'Maintance'),
    )

    ins_id = models.AutoField(primary_key=True, verbose_name="IncidentStep ID")
    ins_type = models.CharField(max_length=1, blank=True, choices=INCIDENT_STEP_TYPE, verbose_name="IncidentStep type")
    ins_inc_id = models.ForeignKey('Incident', blank=True, null=True, verbose_name="IncidentStep incident FK")
    ins_com_id = models.ForeignKey('Comment', blank=True, null=True, verbose_name="IncidentStep comment FK")
    ins_ent_id = models.IntegerField(blank=True, null=True, verbose_name="Connected entity ID")

    def __unicode__(self):
        return str( self.ins_id )


class Maintenance(models.Model):

    mnt_id = models.AutoField(primary_key=True, verbose_name="Maintenance ID")
    mnt_date = models.DateTimeField(null=True, blank=True, verbose_name="Maintenance date")
    mnt_name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Maintenance name")
    mnt_rep_id = models.ForeignKey('Report', null=True, blank=True, verbose_name="Maintenance report FK")
    mnt_prj_id = models.ForeignKey('Project', null=True, blank=True, verbose_name="Maintenance project FK")
    mnt_com_id = models.ForeignKey('Comment', null=True, blank=True, verbose_name="Maintenance comment FK")

    def __unicode__(self):
        return str( self.mnt_id )

class Alert(models.Model):
    ALERT_TYPE = (
        ('B', 'Batch processing'),
        ('C', 'Cron error'),
        ('V', 'Connection problem'),
        ('S', 'Space problem'),
        ('E', 'Monitoring error'),
        ('O', 'Other'),
    )

    alt_id = models.AutoField(primary_key=True, verbose_name="Alert ID")
    alt_date = models.DateTimeField(null=True, blank=True, verbose_name="Alert date")
    alt_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Alert name")
    alt_ticket = models.CharField(max_length=128, null=True, blank=True, verbose_name="Alert ticket link")
    alt_type = models.CharField(max_length=1, null=True, blank=True, choices=ALERT_TYPE, verbose_name="Alert type")
    alt_rep_id = models.ForeignKey('Report', null=True, blank=True, verbose_name="Alert report FK")
    alt_prj_id = models.ForeignKey('Project', null=True, blank=True, verbose_name="Alert project FK")
    alt_com_id = models.ForeignKey('Comment', null=True, blank=True, verbose_name="Alert comment FK")

    def __unicode__(self):
        return str( self.alt_id )


class Contact(models.Model):
    CONTACT_DIRECTION = (
        ('I', 'Incoming'),
        ('O', 'Outcoming'),
    )

    CONTACT_TYPE = (
        ('P', 'Phone'),
        ('E', 'Email'),
        ('O', 'Other'),
    )

    CONTACT_SCOPE = (
        ('I', 'Internal'),
        ('E', 'External'),
    )

    con_id = models.AutoField(primary_key=True, verbose_name="Contact ID")
    con_date = models.DateTimeField(blank=True, null=True, verbose_name="Contact date")
    con_address = models.CharField(max_length=64, blank=True, verbose_name="Contact address/phone number")
    con_direction = models.CharField(max_length=1, blank=True, choices=CONTACT_DIRECTION, verbose_name="Contact direction")
    con_scope = models.CharField(max_length=1, blank=True, choices=CONTACT_SCOPE, verbose_name="Contact scope")
    con_type = models.CharField(max_length=1, blank=True, choices=CONTACT_TYPE, verbose_name="Contact type")
    con_rep_id = models.ForeignKey('Report', blank=True, null=True, verbose_name="Contact report FK")
    con_prj_id = models.ForeignKey('Project', blank=True, null=True, verbose_name="Contact project FK")
    con_com_id = models.ForeignKey('Comment', blank=True, null=True, verbose_name="Contact comment FK")

    def __unicode__(self):
        return str( self.con_id )

class AlertContact(models.Model):
    aco_id = models.AutoField(primary_key=True, verbose_name="Contact report FK")
    aco_alt_id = models.ForeignKey('Alert', blank=True, null=True, verbose_name="AlertContact alert FK")
    aco_con_id = models.ForeignKey('Contact', blank=True, null=True, verbose_name="AlertContact contact FK")

    def __unicode__(self):
        return str( self.aco_id )


class ReportIncident(models.Model):
    rpi_id = models.AutoField(primary_key=True, verbose_name="ReportIncident ID")
    rpi_rep_id = models.ForeignKey('Report', blank=True, null=True, verbose_name="ReportIncident report FK")
    rpi_inc_id = models.ForeignKey('Incident', blank=True, null=True, verbose_name="ReportIncident incident FK")

    def __unicode__(self):
        return str( self.rpi_id )
