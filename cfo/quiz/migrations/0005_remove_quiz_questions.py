# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-09 22:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20170509_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='questions',
        ),
    ]
