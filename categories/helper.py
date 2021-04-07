from datetime import datetime

from movies.models import Movie
from movies.serializers import StatusMovieSerializer

def ExtractMeta(idList, conditions):
	meta = {
		"languages": [],
		"years": [],
		"directors": [],
		"recommended": 0,
		"last_sync": str(datetime.now().isoformat()) + "Z",
		"number_of_docs": len(idList)
	}

	data = [dict(StatusMovieSerializer(Movie.objects.get(id = ID)).data) for ID in idList]
	conditionKeys = list(set([con['key'] for con in conditions]))

	meta['directors'] = list(set([record['director'] for record in data])) # Unique directors
	meta['languages'] = list(set([record['language'] for record in data])) # Unique languages
	meta['years'] = list(set([record['year'] for record in data])) # Unique years

	if "director" in conditionKeys:
		# "director" is a condition
		# Cannot filter for directors
		del meta['directors']
	if "language" in conditionKeys:
		# "language" is a condition
		# Cannot filter for languages
		del meta['languages']
	if "year" in conditionKeys:
		# "year" is a condition
		# Cannot filter for years
		del meta['years']
	meta['recommended'] = len(list(filter(lambda record: record['status'] > 0, data)))
	return meta