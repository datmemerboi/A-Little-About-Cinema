from django.db import models
from django.contrib.postgres.fields import ArrayField

class Movie(models.Model):
	id = models.CharField(primary_key = True, max_length = 210, null = False)
	
	# Movie Data
	title = models.CharField(max_length = 200)
	director = ArrayField(models.CharField(max_length = 100))
	year = models.PositiveIntegerField()
	language = models.CharField(max_length = 15)
	short_title = models.CharField(max_length = 50, null = True, default = None)
	cast = ArrayField(models.CharField(max_length = 100), null = True, default = list)
	poster_url = models.TextField(null = True, default = None)
	
	# Meta Data
	status = models.SmallIntegerField(default = 0)
	why_watch_it = models.TextField(null = True)
	keywords = ArrayField(models.CharField(max_length = 50), null = False, default = list)
	created_at = models.DateTimeField(auto_now_add = True)

	def PushKeyword(self, keyword):
		self.keywords.append(keyword)
	'''
	{
		"id": "Inglourious Basterds (2009)",
		"title": "Inglourious Basterds",
		"director": [
			"Quentin Tarantino"
		],
		"year": 2009,
		"language": "English",
		"short_title": null,
		"cast": [
			"Brad Pitt",
			"Christoph Waltz",
			"Melanie Laurent"
		],
		"poster_url": null,
		"status": 2,
		"why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
		"keywords": [
			"war",
			"action",
			"funny",
			"violent"
		],
		"created_at": "2021-04-13T15:54:14.657173Z"
	}
	'''