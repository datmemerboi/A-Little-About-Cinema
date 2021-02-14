from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class QuickCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'description', 'movie_list']
		read_only_fields = ['id']

class MetaCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'meta']
		read_only_fields = ['id']