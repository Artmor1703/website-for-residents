# Generated by Django 4.1 on 2022-12-29 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_topic_feedback_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='time_quest',
            field=models.DateTimeField(verbose_name='Время вопроса'),
        ),
    ]