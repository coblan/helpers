# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-05-18 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='名称')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
            ],
        ),
    ]