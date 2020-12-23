from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .serializers import MovieSerializer, QuickMovieSerializer

def ApplyFilterToQuery(query, filters):
	if not filters or len(filters) < 1:
		return query
	for conditionKey, conditionVal in filters:
		if conditionKey.lower() == 'language':
			query = query.filter(language = str(conditionVal))
		# Director filter
		if conditionKey.lower() == 'director':
			query = query.filter(director = str(conditionVal))
		# Cast filter
		if conditionKey.lower() == 'cast':
			query = query.filter(cast__icontains = str(conditionVal))
		# Year filter
		if conditionKey.lower() == 'year':
			query = query.filter(year = int(conditionVal))
		# Keywords filter
		if conditionKey.lower() == 'keyword':
			for word in conditionVal:
				query = query.filter(keyword__icontains = word)
	return query

class NewDocHandler(APIView):
	permission_classes = [IsAuthenticated]
	def MinimalRequirementCheck(self, record):
		ID = "{} ({})".format(record['short_title'], record['year'])\
			if 'short_title' in record\
			else "{} ({})".format(record['title'], record['year'])

		return {'title', 'director', 'year', 'language'}.issubset(record) and not Movie.objects.filter(id = ID).exists()

	def CreateMovieRecord(self, record):
		ID = "{} ({})".format(record['short_title'], record['year'])\
			if 'short_title' in record\
			else "{} ({})".format(record['title'], record['year'])
		
		validator = MovieSerializer(data = { 'id': ID, **record })
		if validator.is_valid(raise_exception = True):
			Movie.objects.create(**validator.validated_data)
		return

	def post(self, request, format = None):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'records' in body:
				# Multiple record request
				if len(body['records']) < 1:
					return Response(status = 400)
				# Filtering bad records
				badRecords = list(filter(lambda record: not self.MinimalRequirementCheck(record) , body['records']))
				if len(badRecords) > 0:
					print("There are {} badRecords".format(len(badRecords)))
					return Response(status = 400)
				else:
					for record in body['records']:
						self.CreateMovieRecord(record)
			else:
				# Single record request
				self.CreateMovieRecord(body)
			return Response(status = 201)
		
		except ValidationError:
			print("Data not valid")
			return Response(status = 400)

		except IntegrityError:
			print("Doc with same ID already exists")
			return Response(status = 409)

		except Exception as err:
			print(type(err).__name__)
			print("Exception\n{}".format(err))
			return Response(status = 500)

class RetrieveDocHandler(APIView):
	def get(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			ID = request.query_params.get('id')\
				if request.query_params.get('id')\
				else body['id']\
				if 'id' in body\
				else None
			if ID:
				if type(ID).__name__ == 'list':
					queryset = Movie.objects.filter(id__in = ID)
					serializer = MovieSerializer(queryset, many = True)
				else:
					queryset = Movie.objects.get(id = ID)
					serializer = MovieSerializer(queryset)
				return Response(serializer.data)
			else:
				return Response(status = 400)

		except ObjectDoesNotExist:
			print("Data not found")
			return Response(status = 404)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class MovieViewHandler(APIView):
	def get(self, request):
		if type(request.data).__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			quick = bool(request.query_params.get('quick')) if request.query_params.get('quick') else None
			limit = int(request.query_params.get('limit')) if request.query_params.get('limit') else None

			queryset = ApplyFilterToQuery(Movie.objects.all().order_by('-created_at'), body['filter'])\
				if 'filter' in body\
				else Movie.objects.all().order_by('-created_at')

			if limit:
				queryset = queryset[:limit]
			if quick:
				serializer = QuickMovieSerializer(queryset, many = True)
			else:
				serializer = MovieSerializer(queryset, many = True)
			return Response(serializer.data)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class UpdateHandler(APIView):
	permission_classes = [IsAuthenticated]
	def put(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			ID = request.query_params.get('id')\
				if request.query_params.get('id')\
				else body['id']\
				if 'id' in body\
				else None
			if ID:
				Movie.objects.filter(id = ID).update(**body)
				return Response(status = 200)
			else:
				return Response(status = 400)

		except ObjectDoesNotExist:
			print("No data found")
			return Response(status = 404)

class DeleteHandler(APIView):
	permission_classes = [IsAuthenticated]
	def delete(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			ID = request.query_params.get('id')\
				if request.query_params.get('id')\
				else body['id']\
				if 'id' in body\
				else None
			if ID:
				Movie.objects.get(id = body['id']).delete()
				return Response(status = 200)
			else:
				return Response(status = 400)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class TruncateHandler(APIView):
	permission_classes = [IsAuthenticated]
	def delete(self, request):
		try:
			Movie.objects.all().delete()
			return Response(status = 200)
			
		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)