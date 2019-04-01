from django.db import models


class Tag(models.Model):
    section = models.TextField()

    def __str__(self):
        return self.section


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tag = models.ManyToManyField(Tag, related_name='tags', through='Relationship')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Relationship(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематики статьи'
        verbose_name_plural = 'Тематики статьи'


