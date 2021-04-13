from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Category(models.Model):	
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 200, null = True)
	conditions = ArrayField(models.JSONField())
	movie_list = ArrayField(models.CharField(max_length = 300), null = False, default = list)
	meta = models.JSONField(null = True)
	created_at = models.DateTimeField(auto_now_add = True)

	def PushMovie(self, movieID):
		if movieID not in self.movie_list:
			self.movie_list.append(movieID)

	def ClearMovieList(self):
		self.movie_list = []
	'''
	{
		"id": 1,
		"name": "Tarantino Collection",
		"description": null,
		"conditions": [
			{
				"key": "director",
				"operator": "in",
				"value": "Quentin Tarantino"
			}
		],
		"movie_list": [],
		"meta": {
			"years": [],
			"languages": [],
			"last_sync": "2021-04-13T15:56:14.652173Z",
			"recommended": 0,
			"number_of_docs": 0
		},
		"created_at": "2021-04-13T15:56:14.652173Z"
	}
	'''