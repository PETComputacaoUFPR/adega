from django.db import models
from degree.models import Degree
# Create your models here.
class Admission(models.Model):
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    degree = models.ForeignKey(Degree)

 
