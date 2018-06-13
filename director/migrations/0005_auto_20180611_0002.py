# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 00:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('director', '0004_auto_20180608_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmodel',
            name='detail',
            field=models.TextField(blank=True, verbose_name='详细'),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='kind',
            field=models.CharField(blank=True, max_length=100, verbose_name='种类'),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作者'),
        ),
    ]