# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-15 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0025_auto_20171116_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='asset.Tag'),
        ),
    ]