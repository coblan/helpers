# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-18 05:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_auto_20170720_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecord',
            name='checker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checked_workrecord', to='organize.Employee', verbose_name='\u5ba1\u6838\u4eba'),
        ),
    ]