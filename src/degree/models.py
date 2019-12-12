from django.db import models
from django.contrib.auth.models import User


class Degree(models.Model):
    name = models.CharField(max_length=40)

    code = models.CharField(max_length=40, unique=True)

    manager = models.ForeignKey(User)

#    grids = models.ForeignKey(Grid, 
#            on_delete=models.CASCADE,
#            related_name = "degree",
#            related_query_name = "degree")
#
    def __str__(self):
        return self.name

    def clean_code(self):
        if '/' in self.code:
            raise ValidationError('Valor inválido: O código não pode conter "/"')
