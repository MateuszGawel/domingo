# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domingo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='rep_test',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
