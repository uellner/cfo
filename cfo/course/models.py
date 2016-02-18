from django.db import models
from django.utils.timezone import datetime


class Course(models.Model):
    u"""
        Classe que representa as informações de um curso.
    """
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    summary = models.TextField(max_length=500)
    description = models.TextField('course description')
    logo = models.ImageField(upload_to='courses/%Y/%m/%d', null=True)

    def __str__(self):
        return self.title


class Unit(models.Model):
    u"""
        Classe que representa as informações de uma unidade de curso.
    """
    title = models.CharField(verbose_name="Título", max_length=255)
    summary = models.TextField(verbose_name="Resumo", max_length=500)
    content = models.TextField(verbose_name="Conteudo")
    course = models.ForeignKey(Course)
    logo = models.ImageField(upload_to='units/%Y/%m/%d', null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    u"""
        Classe que representa as informações de uma lição de unidade.
    """
    title = models.CharField(verbose_name="Título", max_length=155)
    lesson_type = models.CharField(verbose_name="Tipo", max_length=155)
    content = models.TextField(verbose_name="Conteudo")
    unit = models.ForeignKey(Unit)
    logo = models.ImageField(upload_to='lessons/%Y/%m/%d', null=True)

    def __str__(self):
        return self.title
