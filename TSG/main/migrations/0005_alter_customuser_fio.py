# Generated by Django 4.1 on 2023-02-22 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_feedback_time_quest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fio',
            field=models.CharField(default='Пользователь', max_length=255, verbose_name='ФИО'),
        ),
    ]
