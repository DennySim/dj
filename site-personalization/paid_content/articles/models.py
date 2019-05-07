from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid_subscription = models.BooleanField(default=False)


class Article(models.Model):
    headline = models.CharField(max_length=50)
    image = models.FileField(upload_to='img/')
    text = models.TextField()
    paid = models.BooleanField(default=False)
