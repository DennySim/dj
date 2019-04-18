from django.db import models

# Create your models here.

from django.db import models
class Route1(models.Model):

    name = models.CharField(max_length=100)

class Route(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class Station(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    routes = models.ManyToManyField(Route, related_name="stations")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Остановка'
        verbose_name_plural = 'Остановки'





