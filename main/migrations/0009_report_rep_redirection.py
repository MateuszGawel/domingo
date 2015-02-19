# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_report_rep_redirection'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='rep_redirection',
            field=models.DateTimeField(null=True, verbose_name='Report redirection check', blank=True),
            preserve_default=True,
        ),
    ]
