# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCurriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.PositiveIntegerField(null=True)),
                ('type_course', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.IntegerField()),
                ('current', models.BooleanField()),
                ('courses', models.ManyToManyField(through='degree.CourseCurriculum', to='course.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=4)),
                ('report_year', models.PositiveIntegerField(blank=True, null=True)),
                ('report_semester', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='curriculum',
            name='degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='degree.Degree'),
        ),
        migrations.AddField(
            model_name='coursecurriculum',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='degree.Curriculum'),
        ),
    ]