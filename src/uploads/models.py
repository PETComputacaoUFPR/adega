from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from os import path
from django.conf import settings


def get_path(instance, filename):
    return '{}/{}/{}'.format(instance.course, instance.id, filename)


class Submission(models.Model):
    author = models.ForeignKey(User)

    historico = models.FileField(upload_to=get_path)
    matricula = models.FileField(upload_to=get_path)

    course = models.CharField(max_length=10, default='21A')

    timestamp = models.DateTimeField(default=timezone.now)

    last = models.BooleanField(default=True)

    processed = models.BooleanField(default=False)

    process_time = models.IntegerField(null=True)

    def path(self):
        return path.join(settings.MEDIA_ROOT, self.course, str(self.id))

    def __str__(self):
        return 'Submission (from: {}, to: {}, on: {})'.format(self.author.first_name,
                                                              self.course,
                                                              self.timestamp)