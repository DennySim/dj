# Generated by Django 2.1.7 on 2019-03-30 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190330_2344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationship',
            options={'verbose_name': 'Тематики статьи', 'verbose_name_plural': 'Тематики статьи'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Основной', 'verbose_name_plural': 'Основной'},
        ),
    ]
