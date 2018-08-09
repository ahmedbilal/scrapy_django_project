"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from article_api.views import *
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # path('', index),

    path('articles', get_articles, name='get_articles'),
    path('articles/by/<str:author>', get_articles_by_author, name='get_articles_by_author'),
    path('articles/of/<str:category>', get_articles_by_category, name='get_articles_by_category'),
    path('articles/on/<str:date>', get_articles_by_date, name='get_articles_by_date'),
    path('articles/with/<str:title>', get_articles_by_title, name='get_articles_by_title'),

    path('authors', get_authors, name='get_authors'),
    path('categories', get_categories, name='get_categories'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='BBC Articles API'))

]
