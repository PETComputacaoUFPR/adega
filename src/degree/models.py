from django.db import models
from django.contrib.auth.models import User


class Degree(models.Model):
    name = models.CharField(max_length=40)

    code = models.CharField(max_length=40)

    manager = models.ForeignKey(User)

    def __str__(self):
        return self.name

    def clean_code(self):
        if '/' in self.code:
            raise ValidationError('Valor inválido: O código não pode conter "/"')
