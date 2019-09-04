from django.conf import settings
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    answer = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.question
