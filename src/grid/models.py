from django.db import models
from degree.models import Degree

class Grid(models.Model):
    version = models.IntegerField()
    degree = models.ForeignKey(Degree,
            on_delete=models.CASCADE,
            related_name = "grids",
            related_query_name = "grids",
            )

    def __str__(self):
        return "Curso: {} Versão: {}".format(self.degree, self.version)
class GridPeriod(models.Model):
    number = models.IntegerField()
    grid = models.ForeignKey(Grid,
            on_delete=models.CASCADE,
            related_name = "period",
            related_query_name = "period"
            )
    
    def __str__(self):
        return "Periodo: {}\nDisciplinas:\n {}".format(self.number,
                self.courses.all())

class GridCourse(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    period = models.ForeignKey(GridPeriod,
            on_delete=models.CASCADE,
            related_name = "courses",
            related_query_name = "courses",
            )

    def __str__(self):
        return "{} {}".format(self.name, self.code)


    #period_type = models.IntegerField()
    
