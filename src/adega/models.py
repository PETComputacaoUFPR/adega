

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=40)

    code = models.CharField(max_length=40)

    manager = models.ForeignKey(User)

    def clean_code(self):
        if '/' in self.code:
            raise ValidationError('Valor inválido: O código não pode conter "/"')


class Professor(models.Model):
    user = models.OneToOneField(User)
