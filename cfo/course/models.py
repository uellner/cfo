from django.db import models
from django.utils.timezone import datetime
from embed_video.fields import EmbedVideoField
from ..user.models import CourseProgress


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

    def start(self, student):
        u"""
            Start a course.
        """
        if not student:
            return False

        course_progress = CourseProgress(
            course=self,
            student=student,
            activity=self.get_start_activity()
        )
        course_progress.save()
        return course_progress.activity

    def get_next_unit(self, current_unit):
        u"""
            Returns the next unit of the course.
        """
        if not current_unit:
            return None

        next_unit = Unit.objects.filter(
            unit=self,
            rank__gt=current_unit.rank
        ).order_by('rank').all()
        return next_unit and next_unit[0] or None

    def get_next_activity(self, student):
        u"""
            Returns the next activity of the course.
        """
        if not student:
            return None

        course_progress = CourseProgress.objects.filter(
            student=student,
            course=self
        )

        if not course_progress:
            return None

        course_progress = course_progress[0]
        next_activity = course_progress.activity.lesson.get_next_activity(
            course_progress.activity
        )
        # Should the lesson is completed we look for the next one.
        if not next_activity:
            next_lesson = course_progress.activity.lesson.unit.get_next_lesson(
                course_progress.activity.lesson
            )
            # Should the unit is completed we look for the next one.
            if not next_lesson:
                next_unit = course_progress.course.get_next_unit(
                    course_progress.activity.lesson.unit
                )
                if not next_unit:
                    # TODO Course has been completed, we should decide what to do.
                    return None

                # Another lesson has been found!
                next_lesson = next_unit.get_first_lesson()
                next_activity = next_lesson.get_first_activity()
            else:
                # Get the first activity of the next lesson
                next_activity = next_lesson.get_first_activity()

        return next_activity


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

    def get_first_lesson(self):
        u"""
            Returns the first lesson of the unit.
        """
        next_lesson = Lesson.objects.filter(
            lesson=self,
        ).order_by('rank').all()
        return next_lesson and next_lesson[0] or None

    def get_next_lesson(self, current_lesson):
        u"""
            Returns the next lesson of the unit.
        """
        if not current_lesson:
            return None

        next_lesson = Lesson.objects.filter(
            unit=self,
            rank__gt=current_lesson.rank
        ).order_by('rank').all()
        return next_lesson and next_lesson[0] or None


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

    def get_first_activity(self):
        u"""
            Returns the first activity of the lesson.
        """
        next_activity = Activity.objects.filter(
            lesson=self,
        ).order_by('rank').all()
        return next_activity and next_activity[0] or None

    def get_next_activity(self, current_activity):
        u"""
            Returns the next activity of the lesson.
        """
        if not current_activity:
            return None

        next_activity = Activity.objects.filter(
            lesson=self,
            rank__gt=current_activity.rank
        ).order_by('rank').all()
        return next_activity and next_activity[0] or None


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

    def finish(self, student):
        u"""
            Finish the activity.
        """
        if not student:
            return None

        course_progress = CourseProgress.objects.filter(
            student=student,
            course=self.lesson.unit.course
        ).all()

        if not course_progress:
            return None

        # Saving progress
        course_progress = course_progress[0]
        course_progress.activity = self
        course_progress.save()

        return course_progress
