from django.db import models
from django.contrib.auth.models import User


def get_path(instance, filename):
    return "./{}".format(filename)




class Degree(models.Model):
    name = models.CharField(max_length=40)

    code = models.CharField(max_length=40)

    manager = models.ForeignKey(User)

    def __str__(self):
        return self.name

    def clean_code(self):
        if '/' in self.code:
            raise ValidationError('Valor inválido: O código não pode conter "/"')


class Grid(models.Model):
    version = models.IntegerField()
    degree = models.ForeignKey(Degree)
    disciplinas = models.FileField(upload_to=get_path)
    prerequisitos = models.FileField(upload_to=get_path)
    equivalencias = models.FileField(upload_to=get_path)
