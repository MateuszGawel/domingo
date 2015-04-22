# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150326_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentstepalert',
            name='isa_alt_id',
        ),
        migrations.RemoveField(
            model_name='incidentstepalert',
            name='isa_ins_id',
        ),
        migrations.DeleteModel(
            name='IncidentStepAlert',
        ),
        migrations.RemoveField(
            model_name='incidentstepcontact',
            name='isc_con_id',
        ),
        migrations.RemoveField(
            model_name='incidentstepcontact',
            name='isc_ins_id',
        ),
        migrations.DeleteModel(
            name='IncidentStepContact',
        ),
        migrations.AddField(
            model_name='incidentstep',
            name='ins_ent_id',
            field=models.IntegerField(null=True, verbose_name='Connected entity ID', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incidentstep',
            name='ins_type',
            field=models.CharField(blank=True, max_length=1, verbose_name='IncidentStep type', choices=[('C', 'Contact'), ('A', 'Alert')]),
            preserve_default=True,
        ),
    ]
