from rest_framework.decorators import api_view
from rest_framework.response import Response
from article_api.serializers import *
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def get_articles(request):
    """Return all articles"""
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_articles_by_author(request, author):
    """Retiurn all articles by {author_name}"""
    if request.method == 'GET':
        articles = Article.objects.filter(author__name__icontains=author)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_authors(request):
    """Return all authors"""
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_categories(request):
    """Return all news categories"""
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_articles_by_category(request, category):
    """Return all articles of {category_name} category"""
    if request.method == 'GET':
        articles = Article.objects.filter(category__name__exact=category)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_articles_by_date(reqeust, date):
    """Return all articles published on {date}"""
    if reqeust.method == 'GET':
        articles = Article.objects.filter(date__exact=date)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_articles_by_title(request, title):
    """Return all articles whose title contain {title}"""
    if request.method == 'GET':
        articles = Article.objects.filter(title__icontains=title)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)