# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-06-07 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui_editor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='desp',
            field=models.TextField(blank=True, verbose_name='说明'),
        ),
    ]