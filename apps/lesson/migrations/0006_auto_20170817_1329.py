# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0005_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='topic',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='lessonset',
            name='topic',
            field=models.CharField(max_length=255),
        ),
    ]
