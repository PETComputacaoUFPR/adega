from django.db import models
from django.core.validators import MinValueValidator
from degree.models import Curriculum

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=255)
    ira = models.FloatField(validators = [MinValueValidator(0)], null = True, blank = True)
    grr = models.CharField(max_length = 15)
    evasion_form = models.CharField(max_length = 255)
    evasion_year = models.PositiveIntegerField(null = True, blank = True)
    evasion_semester = models.PositiveIntegerField(null = True, blank = True)
    current_curriculum = models.ForeignKey(Curriculum)
    klasses = models.ManyToManyField('klass.Klass', through = 'klass.StudentKlass')
