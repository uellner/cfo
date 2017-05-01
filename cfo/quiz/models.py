from django.db import models
import random


class Quiz(models.Model):
    u"""
        Classe que representa um quiz (conjunto de perguntas e respostas).
    """
    course = models.ForeignKey('course.Course', verbose_name="Curso")
    unit = models.ForeignKey('course.Unit', blank=True, null=True, verbose_name="Unidade")
    questions = models.ManyToManyField('quiz.Question', blank=True, verbose_name='Questões')

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"


class Answer(models.Model):
    u"""
        Classe que representa as alternativas de questões.
    """
    description = models.TextField(verbose_name="Alternativa")
    is_correct = models.BooleanField(default=False, verbose_name="Correta?")
    question = models.ForeignKey('quiz.Question', related_name="answers", verbose_name="Questão")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"


class QuestionsManager(models.Manager):
    def random(self, sample=1, units=[1]):
        random_index = random.sample(list(self.filter(units__in=units)), sample)
        if sample > len(random_index):
            return None
        return self.filter(pk__in=list(map(lambda e: e.id, random_index))).all()


class Question(models.Model):
    u"""
        Classe que representa as questões.
    """
    description = models.TextField(verbose_name="Pergunta")
    comment = models.TextField(null=True, blank=True, verbose_name="Comentário")
    units = models.ManyToManyField('course.Unit', blank=True, verbose_name='Unidades')
    objects = QuestionsManager()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    # @classmethod
    # def get_questions_unit_quiz(cls, unit, sample=10):
    #     u"""
    #         Get random questions to unit quiz.
    #     """
    #     if not unit:
    #         return False
    #
    #     course_progress = cls.objects.filter(
    #         course=self,
    #         student=student,
    #         activity=self.get_start_activity()
    #     )
    #     course_progress.save()
    #     return course_progress.activity
