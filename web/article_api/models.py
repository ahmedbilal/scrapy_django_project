from django.db import models
from django.core.exceptions import ObjectDoesNotExist


ARTICLE_BODY_MAX_LEN = int(pow(2, 16))


class Author(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ArticleManager(models.Manager):
    def abk_insert(self, title, category, author, date, body):
        try:
            _author = Author.objects.get(name__exact=author)
        except ObjectDoesNotExist:
            _author = Author(name=author)
            _author.save()

        try:
            _category = Category.objects.get(name__exact=category)
        except ObjectDoesNotExist:
            _category = Category(name=category)
            _category.save()

        self.get_queryset().create(title=title, category=_category, author=_author, date=date, body=body)


class Article(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default='', blank=True, null=True)
    date = models.CharField(max_length=512, blank=True, null=True)
    body = models.CharField(max_length=ARTICLE_BODY_MAX_LEN, blank=True, null=True)
    objects = ArticleManager()

    def __str__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)
