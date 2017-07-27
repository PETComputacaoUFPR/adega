from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length = 255)
    code = models.CharField(max_length = 8)
    credits = models.IntegerField()
    workload = models.FloatField() # Carga horaria   
