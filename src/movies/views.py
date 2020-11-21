from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Movie
from .serializers import MovieSerializer

import json

def CheckMinimalRequirement(record):
	return {'title', 'director', 'year', 'language'}.issubset(record)

def InsertMovieRecordFn(record):
	ID = "{} ({})".format(record['short_title'], record['year'])\
		if 'short_title' in record\
		else "{} ({})".format(record['title'], record['year'])
	
	Movie.objects.create(id = ID, **record)
	return

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def NewDocHandler(request):
	if request.data.__class__.__name__ == 'QueryDict':
		body = request.data.dict()
	else:
		body = request.data

	try:
		if 'multiple' in body and body['multiple']:
			# Multiple request
			if len(body['records']) < 1:
				return Response(status = 400)
			# Filtering bad records
			badRecords = list(filter(lambda record: not CheckMinimalRequirement(record) , body['records']))
			if len(badRecords) > 0:
				print("There are {} badRecords".format(len(badRecords)))
				return Response(status = 400)
			else:
				for record in body['records']:
					InsertMovieRecordFn(record)
		else:
			# Single record request
			InsertMovieRecordFn(body)
		return Response(status = 201)


	except Exception as err:
		print("Exception\n{}".format(err))
		return Response(status = 500)