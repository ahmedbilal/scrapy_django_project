from rest_framework import serializers
from article_api.models import *


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    author_name = serializers.CharField(source='author.name')

    class Meta:
        model = Article
        fields = ('title', 'category_name', 'author_name', 'date', 'body')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']
