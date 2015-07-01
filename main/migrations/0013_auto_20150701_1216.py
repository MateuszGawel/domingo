# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150701_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alt_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Alert name', blank=True),
        ),
    ]
