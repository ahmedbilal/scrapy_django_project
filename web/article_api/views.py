from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from article_api.models import Article, Author, Category
from article_api.serializers import *


@api_view(['GET'])
def get_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_authors(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
