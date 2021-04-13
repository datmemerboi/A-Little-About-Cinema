from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http.request import QueryDict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .serializers import MovieSerializer, QuickMovieSerializer
from utils.filters import ApplyFiltersToQuery

class CreateHandler(APIView):
	permission_classes = [IsAuthenticated]

	def MinimalRequirementCheck(self, record):
		ID = "{} ({})".format(record['short_title'], record['year'])\
			if 'short_title' in record\
			else "{} ({})".format(record['title'], record['year'])

		if Movie.objects.filter(id = ID).exists(): # Movie object with this ID already exists
			return False
		if not {'title', 'director', 'year', 'language'}.issubset(record): # required fields of a movie record
			return False
		
		# Type check
		if not isinstance(record['title'], str) or\
			not isinstance(record['year'], int) or\
			not isinstance(record['language'], str) or\
			(not isinstance(record['director'], str) and not isinstance(record['director'], list)):
			return False
		return True

	def CreateMovieRecord(self, record):
		ID = "{} ({})".format(record['short_title'], record['year'])\
			if 'short_title' in record\
			else "{} ({})".format(record['title'], record['year'])
		
		if isinstance(record['director'], str):
			record['director'] = [record['director']]
		validator = MovieSerializer(data = { 'id': ID, **record })
		if validator.is_valid(raise_exception = True):
			Movie.objects.create(**validator.validated_data)
		return

	def post(self, request, format = None):
		if isinstance(request.data, QueryDict):
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
			print("Exception\n{}".format(err))
			return Response(status = 500)

class RetrieveHandler(APIView):
	def get(self, request):
		if isinstance(request.data, QueryDict):
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
				if isinstance(ID, list):
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

class ViewHandler(APIView):
	def get(self, request):
		try:
			quick = True\
				if request.query_params.get('quick')\
				and request.query_params.get('quick').lower() in ['true', '1']\
				else False
			limit = int(request.query_params.get('limit')) if request.query_params.get('limit') else None
			recommended = True\
				if request.query_params.get('recommended')\
				and request.query_params.get('recommended').lower() in ['true', '1']\
				else False
			watchable = True\
				if request.query_params.get('watchable')\
				and request.query_params.get('watchable').lower() in ['true', '1']\
				else False

			query = Movie.objects.all().order_by('-created_at')

			if watchable:
				query = query.filter(status__gte = 0)
			if recommended:
				query = query.filter(status__gt = 0)
			if limit:
				query = query[:limit]
			if quick:
				serializer = QuickMovieSerializer(query, many = True)
			else:
				serializer = MovieSerializer(query, many = True)
			return Response(serializer.data)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

	def post(self, request):
		if isinstance(request.data, QueryDict):
			body = request.data.dict()
		else:
			body = request.data
		try:
			quick = bool(body['quick']) if 'quick' in body else False
			limit = int(body['limit']) if 'limit' in body else None
			filters = body['filters'] if 'filters' in body else None
			queryset = ApplyFiltersToQuery(Movie.objects.all().order_by('-created_at'), filters)
			
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
		if isinstance(request.data, QueryDict):
			body = request.data.dict()
		else:
			body = request.data
		try:
			ID = request.query_params.get('id')\
				if request.query_params.get('id')\
				else body['id']\
				if 'id' in body\
				else None

			if 'director' in body and isinstance(body['director'], str):
				body['director'] = [body['director']]

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
		if isinstance(request.data, QueryDict):
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