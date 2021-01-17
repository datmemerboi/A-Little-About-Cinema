from rest_framework import serializers

from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = '__all__'

class QuickMovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('id', 'title', 'director', 'year', 'language')
		read_only_fields = ['id']