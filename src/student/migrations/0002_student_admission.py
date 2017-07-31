# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission',
            field=models.ForeignKey(default=None, to='admission.Admission'),
            preserve_default=False,
        ),
    ]
