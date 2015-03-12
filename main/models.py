from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    REPORT_STATUSES = (
        ('O', 'Open'),
        ('F', 'Finished'),
        ('R', 'Removed'),
    )

    rep_id = models.AutoField(primary_key=True, verbose_name="Report ID")
    rep_status = models.CharField(max_length=1, blank=True, choices=REPORT_STATUSES, verbose_name="Report status")
    rep_date_created = models.DateTimeField(blank=True, null=True, verbose_name="Report creation date")
    rep_date_sent = models.DateTimeField(blank=True, null=True, verbose_name="Report sent date")
    rep_date_removed = models.DateTimeField(blank=True, null=True, verbose_name="Report deletion date")
    rep_redirection = models.BooleanField(blank=True, default="false", verbose_name="Report redirection check")
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
    prj_label = models.CharField(max_length=10, blank=True, verbose_name="Project label")
    prj_name = models.CharField(max_length=64, blank=True, verbose_name="Project full name")

    def __unicode__(self):
        return str( self.prj_label ) + " (" + str( self.prj_name ) + ")"


class Incident(models.Model):
    inc_id = models.AutoField(primary_key=True, verbose_name="Incident ID")
    inc_date_start = models.DateTimeField(blank=True, null=True, verbose_name="Incident start date")
    inc_date_end = models.DateTimeField(blank=True, null=True, verbose_name="Incident end date")
    inc_ticket = models.CharField(max_length=100, blank=True, verbose_name="Incident ticket link")
    inc_rep_id = models.ForeignKey('Report', blank=True, null=True, verbose_name="Incident report FK")
    inc_prj_id = models.ForeignKey('Project', blank=True, null=True, verbose_name="Incident project FK")
    inc_com_id = models.ForeignKey("Comment", blank=True, null=True, verbose_name="Incident comment FK")

    def __unicode__(self):
        return str( self.inc_id )


class IncidentStep(models.Model):
    INCIDENT_STEP_TYPE = (
        ('C', 'Contact'),
        ('A', 'Alert'),
        ('M', 'Maintenance'),
        ('O', 'Other'),
    )

    ins_id = models.AutoField(primary_key=True, verbose_name="IncidentStep ID")
    ins_type = models.CharField(max_length=1, blank=True, choices=INCIDENT_STEP_TYPE, verbose_name="IncidentStep type")
    ins_inc_id = models.ForeignKey('Incident', blank=True, null=True, verbose_name="IncidentStep incident FK")
    ins_com_id = models.ForeignKey('Comment', blank=True, null=True, verbose_name="IncidentStep comment FK")

    def __unicode__(self):
        return str( self.ins_id )


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
    alt_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Alert name")
    alt_ticket = models.CharField(max_length=32, null=True, blank=True, verbose_name="Alert ticket link")
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

    con_id = models.AutoField(primary_key=True, verbose_name="Contact ID")
    con_date = models.DateTimeField(blank=True, null=True, verbose_name="Contact date")
    con_address = models.CharField(max_length=64, blank=True, verbose_name="Contact address/phone number")
    con_direction = models.CharField(max_length=1, blank=True, choices=CONTACT_DIRECTION, verbose_name="Contact direction")
    con_internal = models.BooleanField(blank=True, default="false", verbose_name="Contact internal")
    con_type = models.CharField(max_length=1, blank=True, choices=CONTACT_TYPE, verbose_name="Contact type")
    con_rep_id = models.ForeignKey('Report', blank=True, null=True, verbose_name="Contact report FK")
    con_prj_id = models.ForeignKey('Project', blank=True, null=True, verbose_name="Contact project FK")
    con_com_id = models.ForeignKey('Comment', blank=True, null=True, verbose_name="Contact comment FK")

    def __unicode__(self):
        return str( self.con_id )


class IncidentStepAlert(models.Model):
    isa_id = models.AutoField(primary_key=True, verbose_name="IncidentStepAlert ID")
    isa_ins_id = models.ForeignKey('IncidentStep', blank=True, null=True, verbose_name="IncidentStepAlert incidentStep FK")
    isa_alt_id = models.ForeignKey('Alert', blank=True, null=True, verbose_name="IncidentStepAlert alert FK")

    def __unicode__(self):
        return str( self.isa_id )


class IncidentStepContact(models.Model):
    isc_id = models.AutoField(primary_key=True, verbose_name="Contact report FK")
    isc_ins_id = models.ForeignKey('IncidentStep', blank=True, null=True, verbose_name="IncidentStepContact incidentStep FK")
    isc_con_id = models.ForeignKey('Contact', blank=True, null=True, verbose_name="IncidentStepContact contact FK")

    def __unicode__(self):
        return str( self.isc_id )


class AlertContact(models.Model):
    aco_id = models.AutoField(primary_key=True, verbose_name="Contact report FK")
    aco_alt_id = models.ForeignKey('Alert', blank=True, null=True, verbose_name="AlertContact alert FK")
    aco_con_id = models.ForeignKey('Contact', blank=True, null=True, verbose_name="AlertContact contact FK")

    def __unicode__(self):
        return str( self.aco_id )
