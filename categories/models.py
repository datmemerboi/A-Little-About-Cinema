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
			"value": "Quentin Tarantino",
			"operator": "is"
			}
		],
		"movie_list": [],
		"meta": {
			"years": [],
			"languages": [],
			"last_sync": "2021-04-07T12:39:43.816890Z",
			"recommended": 0,
			"number_of_docs": 0
		},
		"created_at": "2021-04-07T11:40:18.096530Z"
	}
	'''