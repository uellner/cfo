# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-23 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_quizprogress_is_reviewed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizprogress',
            old_name='is_reviewed',
            new_name='is_scored',
        ),
    ]
