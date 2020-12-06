from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from movies.models import Movie
from movies.serializers import MovieSerializer, MovieIDSerializer, QuickMovieSerializer
from .models import Category
from .serializers import CategorySerializer, QuickCategorySerializer, MetaCategorySerializer

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
	def MakeFilterQuery(self, key, value):
		if key == 'director':
			return Movie.objects.filter(director = value)
		elif key == 'language':
			return Movie.objects.filter(language = value)
		elif key == 'year':
			return Movie.objects.filter(year = value)
		elif key == 'keywords':
			return Movie.objects.filter(keywords__icontains = value)

	def Sync(self, ID):
		# Get the category
		categoryRef = Category.objects.get(id = ID)
		category = CategorySerializer(categoryRef).data
		conditionalKey = category['condition']['key']
		conditionalValue = category['condition']['value']
		
		# Get Movie IDs
		queryset = self.MakeFilterQuery(conditionalKey, conditionalValue)
		docs = MovieIDSerializer(queryset, many = True).data
		for movie in docs:
			categoryRef.PushMovie(movie['id'])
		categoryRef.SyncMeta()
		categoryRef.save()
		return

	def put(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'id' not in body:
				return Response(status = 400)
			if type(body['id']).__name__ == 'list':
				for ID in body['id']:
					self.Sync(ID)
			else:
				self.Sync(body['id'])
			return Response(status = 200)

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
			if 'id' in body:
				if type(body['id']).__name__ == 'list':
					queryset = Category.objects.filter(id__in = body['id'])
					serializer = CategorySerializer(queryset, many = True)
					return Response(serializer.data)
				else:
					queryset = Category.objects.get(id = body['id'])
					serializer = CategorySerializer(queryset)
					return Response(serializer.data)
			elif 'name' in body:
				queryset = Category.objects.filter(name = body['name'])
				serializer = CategorySerializer(queryset, many = True)
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
		queryset = Category.objects.all()
		serializer = CategorySerializer(queryset, many = True)
		return Response(serializer.data)

class QuickViewHandler(APIView):
	def get(self, request):
		limit = request.GET.get('limit') if request.GET.get('limit') else 50
		queryset = Category.objects.all()[:limit]
		serializer = QuickCategorySerializer(queryset, many = True)
		return Response(serializer.data)

class MetaViewHandler(APIView):
	def get(self, request):
		limit = request.GET.get('limit') if request.GET.get('limit') else 50
		queryset = Category.objects.all()[:limit]
		serializer = MetaCategorySerializer(queryset, many = True)
		return Response(serializer.data)

class ClearListHandler(APIView):
	permission_classes = [IsAuthenticated]
	def put(self, request):
		if request.data.__class__.__name__ == 'QueryDict':
			body = request.data.dict()
		else:
			body = request.data
		try:
			if 'id' not in body:
				return Response(status = 400)
			doc = Category.objects.get(id = body['id'])
			doc.ClearMovieList()
			doc.save()
			return Response(status = 200)
		except ObjectDoesNotExist:
			return Response(status = 404)
		except Exception as err:
			print("Exception\n{}".format(err))
			return Response(status = 500)