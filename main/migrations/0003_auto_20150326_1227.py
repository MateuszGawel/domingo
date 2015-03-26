# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150312_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alt_name',
            field=models.CharField(max_length=256, null=True, verbose_name='Alert name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='alt_ticket',
            field=models.CharField(max_length=128, null=True, verbose_name='Alert ticket link', blank=True),
            preserve_default=True,
        ),
    ]
