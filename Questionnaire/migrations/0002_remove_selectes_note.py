# Generated by Django 4.1.5 on 2023-06-10 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectes',
            name='note',
        ),
    ]
