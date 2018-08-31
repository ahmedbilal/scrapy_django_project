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
5. [Markdown](https://pypi.org/project/Markdown/)

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

## Usage
To run the spider for crawling BBC's website. Enter the following commands on your terminal.
```bash
cd bbcspider
```
```bash
scrapy run news_spider
```
After the running above commands, your database would be filled with BBC's articles. To test the API enter the following commands on your terminal.
```bash
cd ../web
```
```bash
python manage.py runserver
```
The website should be up and running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API
To read about services we provide through our API visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

We provide the following services through our website
1. All Scrapped Articles @ **/articles**
2. All Authors of scrapped articles **/authors**
3. All Categories of scrapped articles **/categories**
4. Articles by a particular author **/articles/by/{author}**
5. Articles of a particular category **/articles/of/{category}**
6. Articles published on a particular date **/articles/on/{date}**
7. Articles having a particular title **/articles/with/{title}**


## Contribution
I am happy to incorporate any contribution in this project. Just make sure your code is formatted according to PEP8 conventions.


## Some Useful Links
1. [PEP8](http://pep8.org)
