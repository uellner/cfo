from django.db import models
from ..user.models import QuizProgress
from ..course.models import Unit
import random


class Quiz(models.Model):
    u"""
        Classe que representa um quiz (conjunto de perguntas e respostas).
    """
    course = models.ForeignKey('course.Course', verbose_name="Curso")
    unit = models.ForeignKey('course.Unit', blank=True, null=True, verbose_name="Unidade")
    questions = models.ManyToManyField('quiz.Question', blank=True, through='QuizQuestion', verbose_name='Questões')

    def __str__(self):
        return "[%d] - %s" % (self.id, self.course.title)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"

    def start(self, student, sample=2, units=[]):
        u"""
            Start a quiz.
        """
        if not student:
            return False

        # Collect all units if the quiz is not for a particulary one
        if not units:
            units = [u.id for u in Unit.objects.filter(course=self.course).all()]

        # save random questions on the new quiz
        for obj in Question.objects.random(sample, units).all():
            quiz_question = QuizQuestion(
                quiz=self,
                question=obj
            )
            quiz_question.save()

        # start quiz progress
        quiz_progress = QuizProgress(
            quiz=self,
            student=student,
            sample=sample,
            answer=0,
            score=0
        )
        quiz_progress.save()
        return quiz_progress


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


class QuizQuestion(models.Model):
    u"""
        Classe que representa as questões de um quiz.
    """
    quiz = models.ForeignKey('quiz.Quiz', verbose_name="Quiz")
    question = models.ForeignKey('quiz.Question', verbose_name="Questão")
    number = models.IntegerField(verbose_name="Número")

    def save(self, *args, **kwargs):
        if not self.id:
            num = QuizQuestion.objects.filter(quiz=self.quiz).count()
            self.number = num + 1
        super(QuizQuestion, self).save(*args, **kwargs)
