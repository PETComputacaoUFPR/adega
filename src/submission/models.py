from django.db import models
from educator.models import Educator
from django.utils import timezone

import os

from django.conf import settings

from degree.models import Degree

from django.dispatch import receiver


from submission.analysis import main as submission_analysis


def get_path(instance, filename):
    return '{}/{}/{}'.format(instance.degree.code, instance.id, filename)


class Submission(models.Model):
    STATUS_ONGOING = 0
    STATUS_FINISHED = 1
    STATUS_FAIL = 2

    STATUS_CHOICES = (
        (STATUS_ONGOING, 'Em andamento'),
        (STATUS_FINISHED, 'Terminado'),
    )

    ANALYSIS_STATUS_CHOICES = (
        (STATUS_ONGOING, 'Executando'),
        (STATUS_FINISHED, 'Terminado'),
        (STATUS_FAIL, 'Falha'),
    )
    author = models.ForeignKey(Educator)

    csv_data_file = models.FileField(upload_to=get_path)

    degree = models.ForeignKey(Degree, related_name='submissions')
    timestamp = models.DateTimeField(default=timezone.now)
    last = models.BooleanField(default=True)
    processed = models.BooleanField(default=False)
    process_time = models.IntegerField(null=True)
    analysis_status = models.IntegerField(
            default=0,
            choices=ANALYSIS_STATUS_CHOICES
            )
    last_error = models.CharField(default="", max_length=4096)
    relative_year = models.IntegerField(null=True)
    relative_semester = models.IntegerField(null=True)
    semester_status = models.IntegerField(null=True, choices=STATUS_CHOICES)
    done_in = models.DateTimeField(null=True)

    class Meta:
        permissions = (
            # ('view_submission', 'Visualizar Relatórios'),
            ('view_course', 'Visualizar disciplinas'),
            ('view_student', 'Visualizar alunos'),
            ('view_degree', 'Visualizar curso'),
            ('view_admission', 'Visualizar turma ingresso'),
            ('view_cepe9615', 'Visualizar  cepe9615')
            )

    def save(self, *args, **kwargs):
        """
        Sobrescrita do metodo save.
        É necesário rescrever o metodo save, para poder obter o id da instancia
        enquanto o modelo ainda não foi salvo no banco de dados.

        """
        if self.id is None:
            csv_data_file = self.csv_data_file
            self.csv_data_file = None
            super(Submission, self).save(*args, **kwargs)
            self.csv_data_file = csv_data_file
            # kwargs.pop('force_insert')
        super(Submission, self).save(*args, **kwargs)


    def path(self):
        return os.path.join(settings.MEDIA_ROOT, self.degree.code, str(self.id))

    def zip_path(self):
        return os.path.join(self.path(), "{}_data.zip".format(self.degree.name))

    def __str__(self):
        return 'Submission (from: {}, to: {}, on: {})'.format(self.author.user.first_name,
                                                              self.degree.name,
                                                              self.timestamp)
    
    def download_allowed(self, user):
        return (user == self.author.user) or user.is_superuser
    
    def set_executing(self):
        self.processed = False
        self.process_time = None
        self.done_in = timezone.now()
        self.analysis_status = 0
        self.save()

    def set_done(self, time):
        self.processed = True
        self.process_time = time
        self.done_in = timezone.now()
        self.analysis_status = 1
        self.save()

    def set_fail(self,time, error_message):
        self.processed = False
        self.process_time = time
        self.done_in = timezone.now()
        self.analysis_status = 2
        self.last_error = error_message
        self.save()
