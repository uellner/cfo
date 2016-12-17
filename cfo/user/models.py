from django.db import models
from django.contrib.auth.models import User
from ..basic_app.models import TimeStampedModel


class Student(models.Model):
    """
        Student users.
    """
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=32, verbose_name='Telefone', null=True, blank=True)
    courses = models.ManyToManyField('course.Course', blank=True, through='CourseProgress', verbose_name='Cursos')

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
