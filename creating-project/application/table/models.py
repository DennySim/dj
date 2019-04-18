from django.db import models

# Create your models here.

from django.db import models


class TableSettings(models.Model):

    name = models.CharField(max_length=50, unique=True)
    width = models.IntegerField()
    ordinal = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordinal']
        verbose_name = 'Наименование поля'
        verbose_name_plural = 'Наименования полей'


class PathToFile(models.Model):

    path = models.FilePathField(max_length=300, path=".")

    class Meta:
        verbose_name = 'Путь к файлу'
        verbose_name_plural = 'Путь к файлу'

    def __str__(self):
        return self.path

    @classmethod
    def get_path(cls):
        return str(cls.objects.first())[2:]

    @classmethod
    def set_path(cls, path):
        return cls.objects.filter().update(path=path)

