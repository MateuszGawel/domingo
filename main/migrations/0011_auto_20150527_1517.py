# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150520_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='inc_rca',
            field=models.BooleanField(default='false', verbose_name='Incident RCA'),
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_status',
            field=models.CharField(blank=True, max_length=1, verbose_name='Report status', choices=[('O', 'Open'), ('C', 'Closed'), ('R', 'Removed')]),
        ),
    ]
