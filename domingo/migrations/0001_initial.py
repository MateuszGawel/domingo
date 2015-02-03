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
                ('alt_id', models.IntegerField(serialize=False, primary_key=True)),
                ('alt_start_date', models.DateTimeField(null=True, blank=True)),
                ('alt_end_date', models.DateTimeField(null=True, blank=True)),
                ('alt_type', models.CharField(max_length=1, blank=True)),
                ('alt_ticket', models.CharField(max_length=32, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('cal_id', models.IntegerField(serialize=False, primary_key=True)),
                ('cal_date', models.DateTimeField(null=True, blank=True)),
                ('cal_direction', models.CharField(max_length=1, blank=True)),
                ('cal_name', models.CharField(max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('dut_id', models.IntegerField(serialize=False, primary_key=True)),
                ('dut_start_date', models.DateTimeField(null=True, blank=True)),
                ('dut_end_date', models.DateTimeField(null=True, blank=True)),
                ('dut_redirection', models.CharField(max_length=1, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prj_id', models.IntegerField(serialize=False, primary_key=True)),
                ('prj_name', models.CharField(max_length=32, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('rep_id', models.IntegerField(serialize=False, primary_key=True)),
                ('rep_status', models.CharField(max_length=1, blank=True)),
                ('rep_send_date', models.DateTimeField(null=True, blank=True)),
                ('rep_remove_date', models.DateTimeField(null=True, blank=True)),
                ('rep_notes', models.TextField(blank=True)),
                ('rep_usr', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='duty',
            name='dut_rep',
            field=models.ForeignKey(blank=True, to='domingo.Report', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='call',
            name='cal_prj',
            field=models.ForeignKey(blank=True, to='domingo.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='call',
            name='cal_rep',
            field=models.ForeignKey(blank=True, to='domingo.Report', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='alt_prj',
            field=models.ForeignKey(blank=True, to='domingo.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='alt_rep',
            field=models.ForeignKey(blank=True, to='domingo.Report', null=True),
            preserve_default=True,
        ),
    ]
