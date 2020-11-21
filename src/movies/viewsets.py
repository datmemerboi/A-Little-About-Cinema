from .models import Movie
from .serializers import MovieSerializer, QuickMovieSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class MovieViewSet(viewsets.ViewSet):
	def list(self, request):
		# print(request.query_params)
		queryset = Movie.objects.all()
		serializer = MovieSerializer(queryset, many = True)
		return Response(serializer.data)

class QuickViewSet(viewsets.ViewSet):
	def list(self, request):
		# print(request.GET.get('format'), request.GET.get('limit'))
		limit = request.GET.get('limit') if request.GET.get('limit') else 50
		queryset = Movie.objects.all().order_by('created_at')[:limit]
		serializer = QuickMovieSerializer(queryset, many = True)
		return Response(serializer.data)