from django.db import models
from django.contrib.auth.models import User
from ..basic_app.models import TimeStampedModel


class Student(models.Model):
    """
        Student users.
    """
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name='Telefone')
    courses = models.ManyToManyField('course.Course', blank=True, through='CourseProgress', verbose_name='Cursos')
    quizzes = models.ManyToManyField('quiz.Quiz', blank=True, through='QuizProgress', verbose_name='Simulados')

    def __str__(self):
        return "%s" % (self.user.get_full_name())

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class CourseProgress(TimeStampedModel):
    """
        Course progress by a student
    """
    course = models.ForeignKey('course.Course')
    student = models.ForeignKey('Student')
    # Saving the current activity
    activity = models.ForeignKey('course.Activity', blank=True)
    # Flag to indicate whether the course is completed or not
    is_completed = models.BooleanField(default=False)

    @property
    def progress_left(self):
        from ..course.models import Activity

        if self.is_completed:
            return '{:.0f}%'.format(100)

        # Returns the sum of activities of past units
        past_unit_activities = Activity.objects.filter(lesson__unit__course=self.course, lesson__unit__rank__lt=self.activity.lesson.unit.rank).count()
        # Returns the sum of activities of past lessons
        past_lesson_activities = Activity.objects.filter(lesson__unit__course=self.course, lesson__rank__lt=self.activity.lesson.rank).count()
        # Returns the sum of past activities of the same lesson
        past_activities = Activity.objects.filter(lesson__unit__course=self.course, lesson=self.activity.lesson, rank__lte=self.activity.rank).count()
        # Returns the sum of activities
        total_activities = Activity.objects.filter(lesson__unit__course=self.course).count()
        percent_activities = min((past_unit_activities + past_lesson_activities + past_activities) / total_activities * 100, 100)
        return '{:.0f}%'.format(percent_activities)

    @property
    def progress_colour(self):
        if self.is_completed:
            return 'success'
        else:
            return 'info'


class QuizProgress(TimeStampedModel):
    u"""
        Quiz progress by a student.
    """
    quiz = models.ForeignKey('quiz.Quiz', verbose_name="Quiz")
    student = models.ForeignKey('user.Student', verbose_name="Estudante")
    # Answers provided by student
    answers = models.ManyToManyField('quiz.Answer', blank=True, verbose_name='Respostas')
    # Quantity of questions for this quiz
    sample = models.IntegerField(default=10, verbose_name="Quantidade de Questões")
    # Questions answered
    progress = models.IntegerField(default=0, verbose_name="Quantidade Respondida")
    # Score based on answers
    score = models.IntegerField(default=0, verbose_name="Desempenho")
    # Flag to indicate whether the quiz is completed or not
    is_completed = models.BooleanField(default=False)
    # Flag to indicate whether the quiz is scored or not
    is_scored = models.BooleanField(default=False)
    # Flag to indicate whether the quiz is reviewed or not
    is_reviewed = models.BooleanField(default=False)

    def save_progress(self, answer):
        u"""
            Save the quiz progress based on student answers.
        """
        if not answer:
            return None
        # add answer
        self.answers.add(answer)
        # walk on progress
        self.progress += 1
        if self.progress == self.sample:
            self.is_completed = True
        # score
        if answer.is_correct:
            self.score += 1

        self.save()

        return self

    def mark_as_scored(self):
        u"""
            Mark the quiz as scored.
        """
        if not self.is_scored:
            self.is_scored = True
            self.save()
        return self

    def mark_as_reviewed(self):
        u"""
            Mark the quiz as reviewed.
        """
        if not self.is_reviewed:
            self.is_reviewed = True
            self.save()
        return self

    @property
    def score_wrong(self):
        u"""
            Gets the wrong answers
        """
        return self.sample - self.score

    @property
    def score_percentage(self):
        u"""
            Gets the percentage score of this quiz
        """
        return '{0:.1%}'.format(self.score / self.sample)
