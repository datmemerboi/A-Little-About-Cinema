import json
import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Category(models.Model):	
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 200, null = True)
	condition = models.JSONField()
	movie_list = ArrayField(models.CharField(max_length = 300), null = False, default = list)
	meta = models.JSONField(null = True)
	created_at = models.DateTimeField(auto_now_add = True)

	def PushMovie(self, movieID):
		if movieID not in self.movie_list:
			self.movie_list.append(movieID)

	def ClearMovieList(self):
		self.movie_list = []

	def SyncMeta(self):
		doc = {
			"number_of_movies": len(self.movie_list),
			"last_sync": str(datetime.datetime.now().isoformat())+"Z"
		}
		self.meta = json.loads(json.dumps(doc))
		print(self.meta)