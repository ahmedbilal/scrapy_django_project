import sys
import os

from os.path import (dirname, abspath, join)
import subprocess

from rest_framework.response import Response
from article_api.serializers import ArticleSerializer, AuthorSerializer, CategorySerializer
from .models import Article, Author, Category
from rest_framework.views import APIView
from django.http import HttpResponse


def scrape_bbc(request):
    bbcspider_path = dirname(abspath(__file__))  # article_api
    bbcspider_path = dirname(bbcspider_path)  # web
    bbcspider_path = dirname(bbcspider_path)  # scrapy_django_project
    bbcspider_path = join(bbcspider_path, "bbcspider")  # bbcspider

    os.system("(cd {path} ; scrapy crawl news_spider)".format(path=bbcspider_path))
    return HttpResponse("Done")


class ArticleList(APIView):
    _filter = "all"

    def get(self, request, author=None, category=None, date=None, title=None):
        articles = Article.objects
        if self._filter == "all":
            articles = articles.all()

        elif self._filter == "by_author_name":
            articles = articles.filter(author__name__icontains=author)

        elif self._filter == "by_category_name":
            articles = articles.filter(category__name__exact=category)

        elif self._filter == "by_date":
            articles = articles.filter(date__exact=date)

        elif self._filter == "by_title":
            articles = articles.filter(title__icontains=title)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class AuthorList(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


