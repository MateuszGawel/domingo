# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150214_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('mnt_id', models.AutoField(serialize=False, verbose_name='Maintenance ID', primary_key=True)),
                ('mnt_date', models.DateTimeField(null=True, verbose_name='Maintenance date', blank=True)),
                ('mnt_name', models.CharField(max_length=256, null=True, verbose_name='Maintenance name', blank=True)),
                ('mnt_com_id', models.ForeignKey(verbose_name='Maintenance comment FK', blank=True, to='main.Comment', null=True)),
                ('mnt_prj_id', models.ForeignKey(verbose_name='Maintenance project FK', blank=True, to='main.Project', null=True)),
                ('mnt_rep_id', models.ForeignKey(verbose_name='Maintenance report FK', blank=True, to='main.Report', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='project',
            name='prj_label',
        ),
        migrations.AlterField(
            model_name='incidentstep',
            name='ins_type',
            field=models.CharField(blank=True, max_length=1, verbose_name='IncidentStep type', choices=[('C', 'Contact'), ('A', 'Alert'), ('M', 'Maintance')]),
            preserve_default=True,
        ),
    ]
