# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0007_auto_20170817_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('lesson', 'page_number')},
        ),
    ]