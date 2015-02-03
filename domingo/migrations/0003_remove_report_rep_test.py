# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domingo', '0002_report_rep_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='rep_test',
        ),
    ]
