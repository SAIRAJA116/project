# Generated by Django 3.2.13 on 2022-04-21 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0008_quiz_drafted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
    ]
