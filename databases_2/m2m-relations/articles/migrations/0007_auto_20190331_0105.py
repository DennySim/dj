# Generated by Django 2.1.7 on 2019-03-30 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20190331_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tags',
            new_name='tag',
        ),
    ]