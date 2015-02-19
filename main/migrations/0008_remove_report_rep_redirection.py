# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150422_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='rep_redirection',
        ),
    ]
