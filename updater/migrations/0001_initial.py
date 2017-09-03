# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-25 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UneconExcelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=250)),
                ('pubDate', models.DateField(verbose_name='Дата публикации на unecon.ru')),
                ('faculty', models.CharField(blank=True, max_length=250)),
                ('scheduleType', models.CharField(blank=True, max_length=45, verbose_name='Тип расписания')),
                ('scheduleForm', models.CharField(max_length=45, verbose_name='Форма обучения')),
                ('scheduleYear', models.CharField(blank=True, max_length=20, verbose_name='Курс обучения')),
                ('parsed', models.BooleanField(default=False)),
            ],
        ),
    ]
