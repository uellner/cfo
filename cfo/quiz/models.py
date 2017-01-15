from django.db import models


class Quiz(models.Model):
    u"""
        Classe que representa um quiz (conjunto de perguntas e respostas).
    """
    course = models.ForeignKey('course.Course', verbose_name="Curso")
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


class Question(models.Model):
    u"""
        Classe que representa as questões.
    """
    description = models.TextField(verbose_name="Pergunta")
    comment = models.TextField(null=True, blank=True, verbose_name="Comentário")
    units = models.ManyToManyField('course.Unit', blank=True, verbose_name='Unidades')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
