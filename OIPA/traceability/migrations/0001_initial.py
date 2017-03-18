# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 00:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('iati', '0002_auto_20170228_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('root_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='ChainError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_location', models.CharField(max_length=255)),
                ('iati_element', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[(b'warning', 'Warning'), (b'error', 'Error')], max_length=255)),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traceability.Chain')),
            ],
        ),
        migrations.CreateModel(
            name='ChainLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[(b'up', 'Upwards'), (b'down', 'Downwards'), (b'both', 'Both directions')], max_length=4)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iati.Activity')),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traceability.Chain')),
                ('parent_activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chain_parent', to='iati.Activity')),
            ],
        ),
    ]
