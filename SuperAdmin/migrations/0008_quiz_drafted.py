# Generated by Django 3.2.13 on 2022-04-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0007_remove_question_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='drafted',
            field=models.BooleanField(default=False),
        ),
    ]
