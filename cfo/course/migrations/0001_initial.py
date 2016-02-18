# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='date published')),
                ('summary', models.TextField(max_length=500)),
                ('description', models.TextField(verbose_name='course description')),
                ('logo', models.ImageField(null=True, upload_to='courses/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=155, verbose_name='Título')),
                ('lesson_type', models.CharField(max_length=155, verbose_name='Tipo')),
                ('content', models.TextField(verbose_name='Conteudo')),
                ('logo', models.ImageField(null=True, upload_to='lessons/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('summary', models.TextField(max_length=500, verbose_name='Resumo')),
                ('content', models.TextField(verbose_name='Conteudo')),
                ('logo', models.ImageField(null=True, upload_to='units/%Y/%m/%d')),
                ('course', models.ForeignKey(to='course.Course')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='unit',
            field=models.ForeignKey(to='course.Unit'),
        ),
    ]
