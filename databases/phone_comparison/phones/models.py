from django.db import models


class Phone(models.Model):
    price = models.TextField()
    brand = models.TextField()
    model = models.TextField()
    color = models.TextField()


class SmartPhone(Phone):
    operating_system = models.TextField()
    screen_matrix = models.TextField()
    cpu = models.TextField()
    ram = models.TextField()


class MobilePhone(Phone):
    fm_radio = models.TextField()
    torch = models.TextField()
