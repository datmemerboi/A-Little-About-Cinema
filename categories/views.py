from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from utils.filters import SingleCondition
from .models import Category
from .serializers import CategorySerializer, QuickCategorySerializer, MetaCategorySerializer
from .helper import ExtractMeta

class CreateHandler(APIView):
	permission_classes = [IsAuthenticated]
	def MinimalRequirementCheck(self, record):
		if not {'name', 'conditions'}.issubset(record): # required fields of a category record
			return False
		for con in record['conditions']:
			if not {'key', 'operator', 'value'}.issubset(con): # required keys of condition object
				return False
			key = con['key']
			opr = con['operator']
			if key in ['keywords', 'cast'] and opr.lower() == "is": # keywords/cast must have "contains", not "is"
				return False
		return not Category.objects.filter(name = record['name']).exists()

	def post(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'name' not in body or 'conditions' not in body:
				return Response(status = 400)
			if type(body['conditions']).__name__ != "list" or len(body['conditions']) < 1:
				return Response(status = 400)
			if self.MinimalRequirementCheck(body):
				Category.objects.create(**body)
				return Response(status = 201)
			else:
				return Response("Minimal requirements not met", status = 400)

		except IntegrityError:
			return Response(status = 409)
			
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

class ViewHandler(APIView):
	def get(self, request):
		try:
			quick = True\
				if request.query_params.get('quick')\
				and request.query_params.get('quick').lower() in ['true', '1']\
				else False
			limit = int(request.query_params.get('limit')) if request.query_params.get('limit') else None
			meta = True\
				if request.query_params.get('meta')\
				and request.query_params.get('meta').lower() in ['true', '1']\
				else False

			queryset = Category.objects.all().order_by('-created_at')

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

	def post(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			quick = bool(body['quick']) if 'quick' in body else False
			limit = int(body['limit']) if 'limit' in body else None
			meta = bool(body['meta']) if 'meta' in body else False
			
			queryset = Category.objects.all().order_by('-created_at')

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

class ResyncHandler(APIView):
	permission_classes = [IsAuthenticated]
	def SyncByID(self, ID):
		record = CategorySerializer(Category.objects.get(id = ID)).data
		# Get the conditions
		conditions = record['conditions']
		query = Movie.objects

		for con in conditions:
			query = SingleCondition(query, con['key'], con['operator'], con['value'])

		data = list(query.values_list('id', flat = True))
		doc = {
			"movie_list": data,
			"meta": ExtractMeta(data, conditions)
		}
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
					return Response(status = 400)
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
				ref = Category.objects.get(id = ID)
				ref.ClearMovieList()
				ref.save()
				return Response(status = 200)
			else:
				return Response(status = 400)

		except ObjectDoesNotExist:
			return Response(status = 404)

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
			if not body:
				return Response(status = 400)
			ID = request.query_params.get('id')\
				if request.query_params.get('id')\
				else body['id']\
				if 'id' in body\
				else None
			if ID:
				Category.objects.update_or_create(id = ID, defaults = body)
				return Response(status = 200)
			else:
				return Response(status = 400)

		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)