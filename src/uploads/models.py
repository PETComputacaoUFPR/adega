from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from os import path
from django.conf import settings

from degree.models import Degree 


def get_path(instance, filename):
    return '{}/{}/{}'.format(instance.course, instance.id, filename)


class Submission(models.Model):
    STATUS_ONGOING = 0
    STATUS_FINISHED = 1

    STATUS = (
        (STATUS_ONGOING, 'Em andamento'),
        (STATUS_FINISHED, 'Terminado'),
    )

    author = models.ForeignKey(User)

    historico = models.FileField(upload_to=get_path)
    matricula = models.FileField(upload_to=get_path)

    degree = models.ForeignKey(Degree)

    timestamp = models.DateTimeField(default=timezone.now)

    last = models.BooleanField(default=True)

    processed = models.BooleanField(default=False)

    process_time = models.IntegerField(null=True)

    relative_year = models.IntegerField(null=True)

    relative_semester = models.IntegerField(null=True)

    semester_status = models.IntegerField(null=True, choices=STATUS)

    done_in = models.DateTimeField(null=True)

    def path(self):
        return path.join(settings.MEDIA_ROOT, self.degree.code, str(self.id))

    def __str__(self):
        return 'Submission (from: {}, to: {}, on: {})'.format(self.author.first_name,
                                                              self.degree.name,
                                                              self.timestamp)

    def set_done(self, time):
        self.processed = True
        self.process_time = time
        self.done_in = timezone.now()

        self.save()
