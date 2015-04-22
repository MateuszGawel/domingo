# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150422_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='inc_rpi_id',
        ),
        migrations.AddField(
            model_name='incident',
            name='inc_status',
            field=models.CharField(blank=True, max_length=1, verbose_name='Incident status', choices=[('O', 'Open'), ('R', 'Resolved'), ('I', 'Invalid')]),
            preserve_default=True,
        ),
    ]
