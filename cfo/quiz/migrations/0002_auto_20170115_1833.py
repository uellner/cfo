# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-15 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20160814_1815'),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='unit',
        ),
        migrations.AddField(
            model_name='question',
            name='units',
            field=models.ManyToManyField(blank=True, to='course.Unit', verbose_name='Unidades'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='Correta?'),
        ),
    ]
