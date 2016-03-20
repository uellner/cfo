# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20160313_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='rank',
            field=models.IntegerField(verbose_name='Ranking', null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='rank',
            field=models.IntegerField(verbose_name='Ranking', null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='rank',
            field=models.IntegerField(verbose_name='Ranking', null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='logo',
            field=models.ImageField(upload_to='course/activities/%Y/%m/%d', null=True),
        ),
    ]
