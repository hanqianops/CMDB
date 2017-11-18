# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-17 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0028_auto_20171116_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='networkdevice',
            old_name='asset',
            new_name='cabinet',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='asset',
            new_name='cabinet',
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='cabinet',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='server',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='server',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
