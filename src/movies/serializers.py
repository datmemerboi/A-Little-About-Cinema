from .models import Movie
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = '__all__'

class QuickMovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('id', 'title', 'director', 'year')
		read_only_fields = ['id']