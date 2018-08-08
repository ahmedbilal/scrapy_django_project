from rest_framework import serializers
from article_api.models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('title', 'category', 'author', 'date', 'body')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']
