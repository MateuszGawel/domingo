# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20150701_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alt_type',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Alert type', choices=[('E', 'Monitoring error'), ('B', 'Batch processing'), ('C', 'Cron error'), ('V', 'Connection problem'), ('S', 'Space problem'), ('O', 'Other')]),
        ),
        migrations.AlterField(
            model_name='incident',
            name='inc_rca',
            field=models.CharField(blank=True, max_length=1, verbose_name='RCA sent', choices=[('S', 'Sent'), ('N', 'Not sent')]),
        ),
    ]
