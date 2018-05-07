from django.db import models
from django.contrib.auth.models import User
from degree.models import Degree

class Educator(models.Model):
	user = models.OneToOneField(User) 
	degree = models.ManyToManyField(Degree) 
	def __str__(self):
			return "{}".format(self.user.username)  
