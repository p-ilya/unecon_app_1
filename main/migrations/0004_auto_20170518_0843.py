# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-18 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_lesson_lcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='tDegree',
            field=models.CharField(default='не определено', max_length=45, verbose_name='Ученая степень'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='tTitle',
            field=models.CharField(default='не определено', max_length=45, verbose_name='Ученое звание'),
            preserve_default=False,
        ),
    ]
