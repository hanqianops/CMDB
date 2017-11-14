# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-05 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0011_auto_20171101_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='business_unit',
        ),
        migrations.AddField(
            model_name='server',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.BusinessUnit', verbose_name='属于的业务线'),
        ),
        migrations.AlterField(
            model_name='server',
            name='switch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.NetworkDevice', verbose_name='所属交换机'),
        ),
    ]