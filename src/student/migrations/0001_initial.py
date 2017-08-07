# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 14:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('degree', '0001_initial'),
        ('klass', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ira', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('grr', models.CharField(max_length=15)),
                ('evasion_form', models.CharField(max_length=255)),
                ('evasion_year', models.PositiveIntegerField(blank=True, null=True)),
                ('evasion_semester', models.PositiveIntegerField(blank=True, null=True)),
                ('current_curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='degree.Curriculum')),
                ('klasses', models.ManyToManyField(through='klass.StudentKlass', to='klass.Klass')),
            ],
        ),
    ]