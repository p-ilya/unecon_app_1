# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-25 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170518_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lGroup',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tTitle',
            field=models.CharField(blank=True, max_length=45, verbose_name='Должность'),
        ),
    ]