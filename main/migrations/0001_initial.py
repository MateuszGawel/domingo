# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('alt_id', models.AutoField(serialize=False, verbose_name='Alert ID', primary_key=True)),
                ('alt_date', models.DateTimeField(null=True, verbose_name='Alert date', blank=True)),
                ('alt_name', models.CharField(max_length=100, verbose_name='Alert name', blank=True)),
                ('alt_ticket', models.CharField(max_length=32, verbose_name='Alert ticket link', blank=True)),
                ('alt_type', models.CharField(blank=True, max_length=1, verbose_name='Alert type', choices=[('B', 'Batch processing'), ('C', 'Cron error'), ('V', 'Connection problem'), ('S', 'Space problem'), ('E', 'Monitoring error'), ('O', 'Other')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlertContact',
            fields=[
                ('aco_id', models.AutoField(serialize=False, verbose_name='Contact report FK', primary_key=True)),
                ('aco_alt_id', models.ForeignKey(verbose_name='AlertContact alert FK', blank=True, to='main.Alert', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('com_id', models.AutoField(serialize=False, verbose_name='Comment ID', primary_key=True)),
                ('com_value', models.TextField(verbose_name='Comment content', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('con_id', models.AutoField(serialize=False, verbose_name='Contact ID', primary_key=True)),
                ('con_date', models.DateTimeField(null=True, verbose_name='Contact date', blank=True)),
                ('con_address', models.CharField(max_length=64, verbose_name='Contact address/phone number', blank=True)),
                ('con_direction', models.CharField(blank=True, max_length=1, verbose_name='Contact direction', choices=[('I', 'Incoming'), ('O', 'Outcoming')])),
                ('con_scope', models.BooleanField(default='false', verbose_name='Contact internal')),
                ('con_type', models.CharField(blank=True, max_length=1, verbose_name='Contact type', choices=[('P', 'Phone'), ('E', 'Email'), ('O', 'Other')])),
                ('con_com_id', models.ForeignKey(verbose_name='Contact comment FK', blank=True, to='main.Comment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('inc_id', models.AutoField(serialize=False, verbose_name='Incident ID', primary_key=True)),
                ('inc_date_start', models.DateTimeField(null=True, verbose_name='Incident start date', blank=True)),
                ('inc_date_end', models.DateTimeField(null=True, verbose_name='Incident end date', blank=True)),
                ('inc_ticket', models.CharField(max_length=100, verbose_name='Incident ticket link', blank=True)),
                ('inc_com_id', models.ForeignKey(verbose_name='Incident comment FK', blank=True, to='main.Comment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncidentStep',
            fields=[
                ('ins_id', models.AutoField(serialize=False, verbose_name='IncidentStep ID', primary_key=True)),
                ('ins_type', models.CharField(blank=True, max_length=1, verbose_name='IncidentStep type', choices=[('C', 'Contact'), ('A', 'Alert'), ('M', 'Maintenance'), ('O', 'Other')])),
                ('ins_com_id', models.ForeignKey(verbose_name='IncidentStep comment FK', blank=True, to='main.Comment', null=True)),
                ('ins_inc_id', models.ForeignKey(verbose_name='IncidentStep incident FK', blank=True, to='main.Incident', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncidentStepAlert',
            fields=[
                ('isa_id', models.AutoField(serialize=False, verbose_name='IncidentStepAlert ID', primary_key=True)),
                ('isa_alt_id', models.ForeignKey(verbose_name='IncidentStepAlert alert FK', blank=True, to='main.Alert', null=True)),
                ('isa_ins_id', models.ForeignKey(verbose_name='IncidentStepAlert incidentStep FK', blank=True, to='main.IncidentStep', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncidentStepContact',
            fields=[
                ('isc_id', models.AutoField(serialize=False, verbose_name='Contact report FK', primary_key=True)),
                ('isc_con_id', models.ForeignKey(verbose_name='IncidentStepContact contact FK', blank=True, to='main.Contact', null=True)),
                ('isc_ins_id', models.ForeignKey(verbose_name='IncidentStepContact incidentStep FK', blank=True, to='main.IncidentStep', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prj_id', models.AutoField(serialize=False, verbose_name='Project ID', primary_key=True)),
                ('prj_label', models.CharField(max_length=10, verbose_name='Project label', blank=True)),
                ('prj_name', models.CharField(max_length=64, verbose_name='Project full name', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('rep_id', models.AutoField(serialize=False, verbose_name='Report ID', primary_key=True)),
                ('rep_status', models.CharField(blank=True, max_length=1, verbose_name='Report status', choices=[('O', 'Open'), ('F', 'Finished'), ('R', 'Removed')])),
                ('rep_date_created', models.DateTimeField(null=True, verbose_name='Report creation date', blank=True)),
                ('rep_date_sent', models.DateTimeField(null=True, verbose_name='Report sent date', blank=True)),
                ('rep_date_removed', models.DateTimeField(null=True, verbose_name='Report deletion date', blank=True)),
                ('rep_redirection', models.BooleanField(default='false', verbose_name='Report redirection check')),
                ('rep_com_id', models.ForeignKey(verbose_name='Report comment FK', blank=True, to='main.Comment', null=True)),
                ('rep_usr_id', models.ForeignKey(verbose_name='Report user FK', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incident',
            name='inc_prj_id',
            field=models.ForeignKey(verbose_name='Incident project FK', blank=True, to='main.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='inc_rep_id',
            field=models.ForeignKey(verbose_name='Incident report FK', blank=True, to='main.Report', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='con_prj_id',
            field=models.ForeignKey(verbose_name='Contact project FK', blank=True, to='main.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='con_rep_id',
            field=models.ForeignKey(verbose_name='Contact report FK', blank=True, to='main.Report', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertcontact',
            name='aco_con_id',
            field=models.ForeignKey(verbose_name='AlertContact contact FK', blank=True, to='main.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='alt_com_id',
            field=models.ForeignKey(verbose_name='Alert comment FK', blank=True, to='main.Comment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='alt_prj_id',
            field=models.ForeignKey(verbose_name='Alert project FK', blank=True, to='main.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='alt_rep_id',
            field=models.ForeignKey(verbose_name='Alert report FK', blank=True, to='main.Report', null=True),
            preserve_default=True,
        ),
    ]
