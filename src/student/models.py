from django.db import models
from django.core.validators import MinValueValidator
from degree.models import Curriculum
from admission.models import Admission
from utils.data import difference_between_semesters

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=255)
    ira = models.FloatField(validators = [MinValueValidator(0)], null = True, blank = True)
    grr = models.CharField(max_length = 15)
    evasion_form = models.CharField(max_length = 255)
    evasion_year = models.PositiveIntegerField(null = True, blank = True)
    evasion_semester = models.PositiveIntegerField(null = True, blank = True)
    current_curriculum = models.ForeignKey(Curriculum)
    admission = models.ForeignKey(Admission)
    klasses = models.ManyToManyField('klass.Klass', through = 'klass.StudentKlass')

    def get_time_in_degree(self):
        if self.evasion_year is not None:
            year_end = self.evasion_year
            if self.evasion_semester is None:
                semester_end = 2
            else:
                semester_end = self.evasion_semester

        year_start = self.admission.year
        semester_start = self.admission.semester
        difference = difference_between_semesters(year_start, semester_start, year_end, semester_end)
        return difference 
