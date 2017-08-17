# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 12:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0004_auto_20170816_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.NullBooleanField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
