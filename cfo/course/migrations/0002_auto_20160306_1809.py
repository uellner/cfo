# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=embed_video.fields.EmbedVideoField(default='http://www.vimeo.com/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='logo',
            field=models.ImageField(null=True, upload_to='course/courses/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='logo',
            field=models.ImageField(null=True, upload_to='course/lessons/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='logo',
            field=models.ImageField(null=True, upload_to='course/units/%Y/%m/%d'),
        ),
    ]
