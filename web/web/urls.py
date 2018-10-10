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
from article_api.views import ArticleList, AuthorList, CategoryList,scrape_bbc
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # path('', index),

    path('articles', ArticleList.as_view(_filter="all"), name='get_articles'),
    path('articles/by/<str:author>', ArticleList.as_view(_filter="by_author_name"), name='get_articles_by_author'),
    path('articles/of/<str:category>', ArticleList.as_view(_filter="by_category_name"), name='get_articles_by_category'),
    path('articles/on/<str:date>', ArticleList.as_view(_filter="by_date"), name='get_articles_by_date'),
    path('articles/with/<str:title>', ArticleList.as_view(_filter="by_title"), name='get_articles_by_title'),
    path('scrape', scrape_bbc, name="scrape_bbc"),
    path('authors', AuthorList.as_view(), name='get_authors'),
    path('categories', CategoryList.as_view(), name='get_categories'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include_docs_urls(title='BBC Articles API'))

]
