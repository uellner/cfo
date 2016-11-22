import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .utils import get_current_user


class NotRemovedObject(models.Manager):
    """ Model manager to list only objects not removed (is_removed = False).
        Used along with RemovedModel Class.
    """
    def get_queryset(self):
        return super(NotRemovedObject, self).get_queryset().filter(is_removed=False)


class EditableModel(models.Model):
    """ Boolean field indicating if an instance of this class might be modified by users
    """
    is_editable = models.BooleanField(null=False, blank=True, default=True)

    class Meta:
        abstract = True


class RemovedModel(models.Model):
    """ Boolean field indicating whether an instance of this class is removed or not
    """
    is_removed = models.BooleanField(null=False, blank=True, default=False, verbose_name="Inativo")
    objects = NotRemovedObject()
    full_objects = models.Manager()

    def delete(self, *args, **kwargs):
        if not self.is_removed:
            self.is_removed = True
            self.save()
        return

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
        Classe abstrata que salva data/hora de criação e modificação de dados
        assim como o usuário que criou ou modificou.

        Para utiliza-la basta extender ela no model, conforme exemplo:

        from ..basic_app.models import TimeStampedModel
        class MyClass(TimeStampedModel):
            ...
    """

    created_at = models.DateTimeField(verbose_name="Criado Em", default=timezone.now)
    modified_at = models.DateTimeField(verbose_name="Modificado Em", auto_now=True)
    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(app_label)s_%(class)s_created', verbose_name="Criado Por")
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(app_label)s_%(class)s_modified', verbose_name="Modificado Por")

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated():
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


def directory_path(instance, filename):
    """
    Função que determina o caminho para salvar um anexo,
    baseado na instância desse anexo. O formato do caminho é:

    {app_label}/{model}/{id}/{year}/{month}/{day}/{hour}/{minute}/{filename}
    """

    content_type = ContentType.objects.get_for_model(instance)
    base_path = '{app_label}/{model}/'.format(**content_type.__dict__)
    base_path = os.path.join(base_path, '{}/%Y/%m/%d/%H/%M/'.format(instance.id))
    base_path = timezone.now().strftime(base_path)
    return os.path.join(base_path, filename)


class AttachmentModel(TimeStampedModel):
    """
        Classe abstrata que representa anexos no sistema.

        Para utiliza-la basta extender ela no model, conforme exemplo:

        from ..basic_app.models import AttachmentModel
        class MyClass(AttachmentModel):
            ...
    """
    summary = models.CharField(verbose_name="Nome", max_length=256)
    attachment = models.FileField(verbose_name="Arquivo", upload_to=directory_path)

    def __str__(self):
        return self.summary

    def filename(self):
        return "%s" % os.path.basename(self.attachment.name)

    class Meta:
        abstract = True


class ImageModel(TimeStampedModel):
    """
        Classe abstrata que representa imagens no sistema.

        Para utiliza-la basta extender ela no model, conforme exemplo:

        from ..basic_app.models import ImageModel
        class MyClass(ImageModel):
            ...
    """
    summary = models.CharField(verbose_name="Nome", max_length=256)
    image = models.ImageField(verbose_name="Imagem", upload_to=directory_path)

    def __str__(self):
        return self.summary

    def filename(self):
        return "%s" % os.path.basename(self.image.name)

    class Meta:
        abstract = True

    def remove(self):
        """ Remove this image from the database and from filesystem. """
        self.image.storage.delete(self.image.path)
        self.delete()

    def remove_url(self):
        """ Return the url from which this image can be removed. """
        return ''


# TODO: Generalize datetime ossociation accross all models
# TODO: ref [http://stackoverflow.com/questions/20895429/how-exactly-do-django-content-types-work]
# TODO: ref [https://docs.djangoproject.com/ja/1.9/ref/contrib/contenttypes/]
# class DateTime(models.Model):
#     """ Stores date and times from all over the system
#     """
#     model = models.CharField(verbose_name="Modelo", max_length=255)
#     cause = models.CharField(verbose_name="Motivo", max_length=255)
#     foreignk = models.IntegerField()
#     datetime = models.DateTimeField(verbose_name="Data/Hora", default=django.utils.timezone.now)
