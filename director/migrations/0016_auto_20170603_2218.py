# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-03 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('director', '0015_auto_20170603_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmodel',
            name='kind',
            field=models.CharField(blank=True, max_length=100, verbose_name='\u79cd\u7c7b'),
        ),
    ]
