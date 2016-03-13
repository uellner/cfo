# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20160306_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Título', max_length=155)),
                ('activity_type', models.CharField(verbose_name='Tipo', max_length=155)),
                ('content', models.TextField(verbose_name='Conteudo')),
                ('logo', models.ImageField(upload_to='course/activity/%Y/%m/%d', null=True)),
                ('video', embed_video.fields.EmbedVideoField(default='http://www.vimeo.com/')),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='content',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_type',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='video',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='content',
        ),
        migrations.AddField(
            model_name='lesson',
            name='summary',
            field=models.TextField(verbose_name='Resumo', default='resumo teste', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='lesson',
            field=models.ForeignKey(to='course.Lesson'),
        ),
    ]
