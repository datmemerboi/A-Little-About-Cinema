from django.db import models
from django.contrib.postgres.fields import ArrayField

class Movie(models.Model):
	id = models.CharField(primary_key = True, max_length = 210, null = False)
	
	# Movie Data
	title = models.CharField(max_length = 200)
	director = models.CharField(max_length = 100)
	year = models.PositiveIntegerField()
	language = models.CharField(max_length = 15)
	short_title = models.CharField(max_length = 50, null = True, default = None)

	# Meta Data
	status = models.SmallIntegerField(default = 0)
	why_watch_it = models.TextField(null = True)
	keywords = ArrayField(models.CharField(max_length = 50), null = False, default = list)
	created_at = models.DateTimeField(auto_now_add = True)

	def PushKeyword(self, keyword):
		self.keywords.append(keyword)