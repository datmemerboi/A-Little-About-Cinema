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

	meta['directors'] = list(set([record['director'][0] for record in data])) # Unique directors
	meta['languages'] = list(set([record['language'] for record in data])) # Unique languages
	meta['years'] = list(set([record['year'] for record in data])) # Unique years

	for con in conditions:
		key = con['key']
		opr = con['operator']
		val = con['value']
		if key == "director" and (opr == "in" or copr == "contains") and len(val) == 1:
			# All records have the same director
			del meta['directors']
		if key == "language" and (opr == "is" or opr == "equals"):
			# All records have the same language
			del meta['languages']
		if key == "year" and (opr == "is" or opr == "equals"):			
			# All records have the same year
			del meta['years']

	meta['recommended'] = len(list(filter(lambda record: record['status'] > 0, data)))
	return meta