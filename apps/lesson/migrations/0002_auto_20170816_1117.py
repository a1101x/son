# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lesson.LessonSet'),
        ),
    ]
