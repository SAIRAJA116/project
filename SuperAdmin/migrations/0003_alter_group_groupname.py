# Generated by Django 3.2.13 on 2022-04-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0002_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='groupName',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
