# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-04 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iati_codelists', '0002_auto_20151223_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
    ]
