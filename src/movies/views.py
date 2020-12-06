from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .serializers import MovieSerializer, QuickMovieSerializer

class NewDocHandler(APIView):
	permission_classes = [IsAuthenticated]
	def CheckMinimalRequirement(self, record):
		return {'title', 'director', 'year', 'language'}.issubset(record)

	def InsertMovieRecord(self, record):
		ID = "{} ({})".format(record['short_title'], record['year'])\
			if 'short_title' in record\
			else "{} ({})".format(record['title'], record['year'])
		
		if not Movie.objects.filter(id = ID).exists():
			Movie.objects.create(id = ID, **record)
		return

	def post(self, request, format = None):
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
				badRecords = list(filter(lambda record: not self.CheckMinimalRequirement(record) , body['records']))
				if len(badRecords) > 0:
					print("There are {} badRecords".format(len(badRecords)))
					return Response(status = 400)
				else:
					for record in body['records']:
						self.InsertMovieRecord(record)
			else:
				# Single record request
				self.InsertMovieRecord(body)
			return Response(status = 201)
		
		except IntegrityError:
			print("Doc with same ID already exists")
			return Response(status = 409)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class RetrieveDocHandler(APIView):
	def get(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'id' not in body:
				return Response(status = 400)
			if type(body['id']).__name__ == 'list':
				queryset = Movie.objects.filter(id__in = body['id'])
				serializer = MovieSerializer(queryset, many = True)
			else:
				queryset = Movie.objects.get(id = body['id'])
				serializer = MovieSerializer(queryset)
			return Response(serializer.data)

		except ObjectDoesNotExist:
			print("Data not found")
			return Response(status = 404)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class MovieViewHandler(APIView):
	def get(self, request):
		queryset = Movie.objects.all()
		serializer = MovieSerializer(queryset, many = True)
		return Response(serializer.data)

class QuickViewHandler(APIView):
	def get(self, request):
		limit = request.GET.get('limit') if request.GET.get('limit') else 50
		queryset = Movie.objects.all().order_by('created_at')[:limit]
		serializer = QuickMovieSerializer(queryset, many = True)
		return Response(serializer.data)

class UpdateHandler(APIView):
	permission_classes = [IsAuthenticated]
	def put(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'id' not in body:
				return Response(status = 400)
			Movie.objects.filter(id = body['id']).update(**body)
			return Response(status = 200)

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
			if 'id' not in body:
				return Response(status = 400)
			Movie.objects.get(id = body['id']).delete()
			return Response(status = 200)
		
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