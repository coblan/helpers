# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-20 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('director', '0020_auto_20170630_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='permitmodel',
            name='desp',
            field=models.TextField(blank=True, verbose_name='\u63cf\u8ff0'),
        ),
    ]
