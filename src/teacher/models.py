from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, null=True)
    degrees = models.ManyToManyField('degree.Degree', related_name="teachers")
    coordinations = models.ForeignKey('degree.Degree', related_name="coordinators", null=True, blank=True)
