from django.db import models
from django.db.models import Max
from course.models import Course
# Create your models here.
class Degree(models.Model):
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 4)
    report_year = models.PositiveIntegerField(null = True, blank = True)
    report_semester = models.PositiveIntegerField(null = True, blank = True)

class Curriculum(models.Model):
    degree = models.ForeignKey(Degree)
    start_year = models.IntegerField()
    courses = models.ManyToManyField(Course, through='CourseCurriculum')
    current = models.BooleanField()

    def get_amount_of_semesters(self):
        max_period = CourseCurriculum.objecs.filter(curriculum = self).aggregate(Max('period'))
        return max_period['period__max']

class CourseCurriculum(models.Model):
    curriculum = models.ForeignKey(Curriculum)
    course = models.ForeignKey(Course)
    period = models.PositiveIntegerField(null = True)
    type_course = models.CharField(max_length = 255)
