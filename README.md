![Django + Scrapy](https://image.ibb.co/iNEpYU/django_plus_scrapy.png)

Fetches/Parses articles from [BBC](http://www.bbc.com/)'s website and insert it into database connected with our django application that provide
api access to these articles. It is created as a project during Arbisoft's 6 week internship program. It fetches 
upto five pages (This limit is placed to shorter the time of scrapping. If you want to increase the limit you can update
the *MAX_PAGES* constant in bbcspider/bbcspider/spiders/news_spider.py) of the following BBC articles categories.
1. Travel
2. Capital
3. Culture
4. Weather
5. Autos
6. Future
7. Earth

and restrict itself to Homepage of the following categories (due to further multiple categories of each of them).
1. News
2. Sports

After parsing is done, all these articles are inserted in our database one by one.

## Dependencies
1. [Scrapy](https://scrapy.org/)
2. [Django](https://www.djangoproject.com/)
3. [Requests](http://docs.python-requests.org/en/master/)
4. [Django Rest Framework](http://www.django-rest-framework.org/)

## Installation
The easiest way is to clone/download the repository. Run the following commands on your terminal to clone the repository.
```bash
   git clone https://github.com/ahmedbilal/scrapy_django_project.git
```
```bash
   cd scrapy_django_project
```
```bash
   pip install -r requirements.txt
```
and you are **done**
