from django.db import models
from course.models import Course
from student.models import Student

# Create your models here.
class Klass(models.Model):
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    course = models.ForeignKey(Course)
    letter = models.CharField(max_length = 1, null = True, blank = True)

class StudentKlass(models.Model):
    grade = models.FloatField(null=True, blank=True)
    situation = models.CharField(max_length = 255)
    student = models.ForeignKey(Student)
    klass = models.ForeignKey(Klass)
