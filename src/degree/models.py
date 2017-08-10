from django.db import models
from django.db.models import Max
from course.models import Course
from mongoengine import Document, EmbeddedDocument, fields

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
        max_period = CourseCurriculum.objects.filter(curriculum = self).aggregate(Max('period'))
        return max_period['period__max']

class CourseCurriculum(models.Model):
    curriculum = models.ForeignKey(Curriculum)
    course = models.ForeignKey(Course)
    period = models.PositiveIntegerField(null = True)
    type_course = models.CharField(max_length = 255)

class CourseCurriculumMongo(Document):
    start_year = fields.IntField()

class CurriculumMongo(Document):
    courses = fields.ListField(fields.EmbeddedDocumentField('CourseCurriculumMongo'))


class DegreeMongo(Document):
    name = fields.StringField(max_length=50)
    curriculum = fields.ListField(fields.EmbeddedDocumentField('CurriculumMongo'))
