from rest_framework import serializers

from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = '__all__'

class QuickMovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('id', 'title', 'director', 'year')
		read_only_fields = ['id']

class MovieIDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ['id']