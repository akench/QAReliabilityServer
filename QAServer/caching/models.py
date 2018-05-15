from django.db import models
from datetime import datetime

# Create your models here.
class Report(models.Model):
	site = models.CharField(max_length=100)
	url = models.CharField(max_length=500)
	question = models.TextField()
	answer = models.TextField()
	created_date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.site + ": " + self.url