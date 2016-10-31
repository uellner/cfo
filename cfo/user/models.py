from django.db import models
from django.contrib.auth.models import User


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


class CourseProgress(models.Model):
    """
        Course progress by a student
    """
    course = models.ForeignKey('course.Course')
    student = models.ForeignKey('Student')
    # Saving the current activity
    activity = models.ForeignKey('course.Activity', blank=True)
