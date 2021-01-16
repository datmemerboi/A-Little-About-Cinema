from datetime import datetime

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from movies.serializers import QuickMovieSerializer
from .models import Category
from .serializers import CategorySerializer, QuickCategorySerializer, MetaCategorySerializer
from .filters import SingleConditionFilter, MultiConditionFilter

class NewCategoryHandler(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data

		try:
			if 'name' not in body or 'condition' not in body:
				return Response(status = 400)
			Category.objects.create(**body)
			return Response(status = 201)

		except IntegrityError:
			return Response(status = 409)
			
		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class ResyncHandler(APIView):
	permission_classes = [IsAuthenticated]

	def ExtractStatsFromList(self, idList, condition):
		if type(condition).__name__ == "list":
			# Stats for multiple conditions
			return {
				"last_sync": str(datetime.now().isoformat()) + "Z",
				"number_of_docs": len(idList)
			}
		else:
			key = condition['key']
			print(key)
			meta = {}
			if key == 'director':
				# Language, Year, Status stats
				meta = { 'languages': {}, 'years': {}, 'recommended': 0 }
				for ID in idList:
					data = dict(QuickMovieSerializer(Movie.objects.get(id = ID)).data)
					if data['language'] in meta['languages']:
						meta['languages'][data['language']] += 1
					else:
						meta['languages'][data['language']] = 1
					if data['year'] in meta['years']:
						meta['years'][data['year']] += 1
					else:
						meta['years'][data['year']] = 1
					if 'status' in data and data['status'] > -1:
						meta['recommended'] += 1

			elif key == 'year':
				# Director, Language, Status stats
				meta = { 'directors': {}, 'languages': {}, 'recommended': 0 }
				for ID in idList:
					data = dict(QuickMovieSerializer(Movie.objects.get(id = ID)).data)
					if data['language'] in meta['languages']:
						meta['languages'][data['language']] += 1
					else:
						meta['languages'][data['language']] = 1
					if data['director'] in meta['directors']:
						meta['directors'][data['director']] += 1
					else:
						meta['directors'][data['director']] = 1
					if 'status' in data and data['status'] > -1:
						meta['recommended'] += 1

			elif key == 'language':
				# Director, Year, Status stats
				meta = { 'directors': {}, 'years': {}, 'recommended': 0 }
				for ID in idList:
					data = dict(QuickMovieSerializer(Movie.objects.get(id = ID)).data)
					if data['director'] in meta['directors']:
						meta['directors'][data['director']] += 1
					else:
						meta['directors'][data['director']] = 1
					if data['year'] in meta['years']:
						meta['years'][data['year']] += 1
					else:
						meta['years'][data['year']] = 1
					if 'status' in data and data['status'] > -1:
						meta['recommended'] += 1
			meta = {
				"last_sync": str(datetime.now().isoformat()) + "Z",
				"number_of_docs": len(idList),
				**meta
			}
			print(meta, "after sync")
			return meta

	def SyncByID(self, ID):
		record = CategorySerializer(Category.objects.get(id = ID)).data
		# Get the condition
		condition = record['condition']
		query = Movie.objects
		if type(condition).__name__ == "list":
			query = MultiConditionFilter(query, condition)
		else:
			query = SingleConditionFilter(query, condition['key'], condition['operator'], condition['value'])
		'''


		Check and avoid cast equal or keywords equal!



		'''
		data = list(query.values_list('id', flat = True))
		doc = {
			"movie_list": data,
			"meta": self.ExtractStatsFromList(data, condition)
		}
		print(doc)
		Category.objects.update_or_create(id = ID, defaults = doc)
		return 

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
				if type(ID).__name__ == 'list':
					return Response(status = 202)
				else:
					self.SyncByID(ID)
					return Response(status = 200)
			else:
				return Response(status = 400)

		except ObjectDoesNotExist:
			return Response(status = 404)
		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class RetrieveHandler(APIView):
	def get(self, request):
		if type(request.data).__name__ == 'QueryDict':
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
					queryset = Category.objects.filter(id__in = ID)
					serializer = CategorySerializer(queryset, many = True)
				else:
					queryset = Category.objects.get(id = ID)
					serializer = CategorySerializer(queryset)
				return Response(serializer.data)
			else:
				return Response(status = 400)
		
		except ObjectDoesNotExist:
			return Response(status = 404)
		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class CategoryViewHandler(APIView):
	def get(self, request):
		try:
			quick = True if request.query_params.get('quick') and request.query_params.get('quick').lower() in ['true', '1'] else False
			limit = int(request.query_params.get('limit')) if request.query_params.get('limit') else None
			meta = True if request.query_params.get('meta') and request.query_params.get('meta').lower() in ['true', '1'] else False
			queryset = Category.objects.all()
			if limit:
				queryset = queryset[:limit]
			if meta:
				serializer = MetaCategorySerializer(queryset, many = True)
			elif quick:
				serializer = QuickCategorySerializer(queryset, many = True)
			else:
				serializer = CategorySerializer(queryset, many = True)
			return Response(serializer.data)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)

class ClearListHandler(APIView):
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
				doc = Category.objects.get(id = ID)
				doc.ClearMovieList()
				doc.save()
				return Response(status = 200)
			else:
				return Response(status = 400)

		except ObjectDoesNotExist:
			return Response(status = 404)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)