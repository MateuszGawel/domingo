# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150701_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='rep_date_removed',
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_status',
            field=models.CharField(blank=True, max_length=1, verbose_name='Report status', choices=[('O', 'Open'), ('C', 'Closed')]),
        ),
    ]
