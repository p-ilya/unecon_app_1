# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170108_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lComment',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
