from django.db import models
from django.template.defaultfilters import slugify


class Phone(models.Model):

    name = models.TextField()
    slug = models.SlugField(default=None)
    price = models.FloatField()
    image = models.TextField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)

