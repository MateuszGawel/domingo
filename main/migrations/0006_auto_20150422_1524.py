# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150422_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportIncident',
            fields=[
                ('rpi_id', models.AutoField(serialize=False, verbose_name='ReportIncident ID', primary_key=True)),
                ('rpi_inc_id', models.ForeignKey(verbose_name='ReportIncident incident FK', blank=True, to='main.Incident', null=True)),
                ('rpi_rep_id', models.ForeignKey(verbose_name='ReportIncident report FK', blank=True, to='main.Report', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='incident',
            name='inc_rep_id',
        ),
        migrations.AddField(
            model_name='incident',
            name='inc_rpi_id',
            field=models.ForeignKey(verbose_name='Incident reportIncident FK', blank=True, to='main.ReportIncident', null=True),
            preserve_default=True,
        ),
    ]
