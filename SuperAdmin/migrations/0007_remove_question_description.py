# Generated by Django 3.2.13 on 2022-04-20 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0006_quiz_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='description',
        ),
    ]
