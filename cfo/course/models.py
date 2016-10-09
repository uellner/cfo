from django.db import models
from django.utils.timezone import datetime
from embed_video.fields import EmbedVideoField


class Course(models.Model):
    u"""
        Classe que representa as informações de um curso.
    """
    title = models.CharField(max_length=255, verbose_name="Título")
    pub_date = models.DateTimeField('Data de Publicação', default=datetime.now)
    summary = models.TextField(max_length=500, verbose_name="Resumo")
    description = models.TextField(verbose_name="Descrição")
    logo = models.ImageField(upload_to='course/courses/%Y/%m/%d', null=True, verbose_name="Logo")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def get_start_activity(self):
        u"""
            Returns the start activity of the course.
        """
        first_unit = Unit.objects.filter(course=self).order_by('rank').first()
        first_lesson = Lesson.objects.filter(unit=first_unit).order_by('rank').first()
        start_activity = Activity.objects.filter(lesson=first_lesson).order_by('rank').first()
        return start_activity


class Unit(models.Model):
    u"""
        Classe que representa as informações de uma unidade de curso.
    """
    title = models.CharField(verbose_name="Título", max_length=255)
    summary = models.TextField(verbose_name="Resumo", max_length=500)
    rank = models.IntegerField(verbose_name="Ranking", null=True)
    course = models.ForeignKey(Course, verbose_name="Curso")
    logo = models.ImageField(upload_to='course/units/%Y/%m/%d', null=True, blank=True, verbose_name="Logo")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"


class Lesson(models.Model):
    u"""
        Classe que representa as informações de uma lição de unidade.
    """
    title = models.CharField(verbose_name="Título", max_length=155)
    summary = models.TextField(verbose_name="Resumo", max_length=500)
    rank = models.IntegerField(verbose_name="Ranking", null=True)
    unit = models.ForeignKey(Unit, verbose_name="Unidade")
    logo = models.ImageField(upload_to='course/lessons/%Y/%m/%d', null=True, blank=True, verbose_name="Logo")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lição"
        verbose_name_plural = "Lições"


class Activity(models.Model):
    u"""
        Classe que representa as informações de atividade de uma lição.
    """
    title = models.CharField(verbose_name="Título", max_length=155)
    activity_type = models.CharField(verbose_name="Tipo", max_length=155)
    content = models.TextField(verbose_name="Conteudo")
    rank = models.IntegerField(verbose_name="Ranking", null=True)
    lesson = models.ForeignKey(Lesson, verbose_name="Lição")
    logo = models.ImageField(upload_to='course/activities/%Y/%m/%d', null=True, blank=True, verbose_name="Logo")
    video = EmbedVideoField(default='http://www.vimeo.com/', verbose_name="Video")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def get_rank_choices():
        return [(x, x) for x in Activity.objects.count()]
