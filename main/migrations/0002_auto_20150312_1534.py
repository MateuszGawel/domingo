# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alt_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Alert name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='alt_ticket',
            field=models.CharField(max_length=32, null=True, verbose_name='Alert ticket link', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='alt_type',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Alert type', choices=[('B', 'Batch processing'), ('C', 'Cron error'), ('V', 'Connection problem'), ('S', 'Space problem'), ('E', 'Monitoring error'), ('O', 'Other')]),
            preserve_default=True,
        ),
    ]
