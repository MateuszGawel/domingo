# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150527_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alt_name',
            field=models.CharField(max_length=2, null=True, verbose_name='Alert name', blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='con_scope',
            field=models.CharField(blank=True, max_length=1, verbose_name='Contact scope', choices=[('I', 'Internal'), ('E', 'External')]),
        ),
        migrations.AlterField(
            model_name='incident',
            name='inc_rca',
            field=models.BooleanField(default='False', verbose_name='Incident RCA'),
        ),
    ]
