from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
        Student users.
    """
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=32, verbose_name='Telefone', null=True, blank=True)

    def __str__(self):
        return "%s" % (self.user.get_full_name())

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
