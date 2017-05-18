# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-17 15:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WxInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=30, unique=True, verbose_name=b'openid')),
                ('head', models.CharField(blank=True, max_length=300, verbose_name=b'head')),
                ('nickname', models.CharField(blank=True, max_length=200, verbose_name=b'nick name')),
                ('sex', models.CharField(blank=True, max_length=10, verbose_name=b'sex')),
                ('province', models.CharField(blank=True, max_length=50, verbose_name=b'province')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name=b'city')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name=b'country')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
            ],
        ),
    ]
