# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-16 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170616_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='tPhoto',
            field=models.CharField(blank=True, max_length=30, verbose_name='Фотография'),
        ),
    ]
