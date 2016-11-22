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

    @property
    def progress_left(self):
        from ..course.models import Activity
        # Returns the percent progress of the course based on current rank acitivity.
        completed_activities = Activity.objects.filter(lesson__unit__course=self.course, rank__lte=self.activity.rank).count()
        total_activities = Activity.objects.filter(lesson__unit__course=self.course).count()
        percent_activities = min(completed_activities / total_activities * 100, 100)
        return '{:.0f}%'.format(percent_activities)
