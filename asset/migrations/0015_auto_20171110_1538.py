# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-10 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0014_auto_20171105_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='device_status_id',
        ),
        migrations.AddField(
            model_name='server',
            name='device_status_id',
            field=models.IntegerField(choices=[(0, '在线'), (1, '已下线'), (2, '未知'), (3, '故障'), (4, '备用')], default=1, verbose_name='状态'),
        ),
    ]
