# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-27 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0006_auto_20180924_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
