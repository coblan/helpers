# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-04 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('director', '0017_auto_20191204_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kvmodel',
            name='key',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='key'),
        ),
    ]