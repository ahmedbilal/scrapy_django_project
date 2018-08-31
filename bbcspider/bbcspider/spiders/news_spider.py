"""
    Fetches/Parses articles from BBC's website and
    insert it into database connected with our django
    application that provide public api access to these
    articles
"""

import sys
import os
from os.path import (dirname, abspath)

from urllib.parse import urljoin
import django
import requests
import scrapy

PROJECT_ROOT = dirname(dirname(dirname(dirname(abspath(__file__)))))

sys.path.insert(0, os.path.join(PROJECT_ROOT, "web"))
os.environ["DJANGO_SETTINGS_MODULE"] = 'web.settings'
django.setup()

from article_api.models import Article, Author, Category


"""
Category Name   -   Link Collection -   Data Extraction
1. Travel       -   Done            -   Done
2. News         -   Done (Only Home)-   Done
3. Capital      -   Done            -   Done
4. Arts         -   Done (Some bugs)-   Not Done (some flaws)
5. Sport        -   Done (Only Home)-   Done
6. Culture      -   Done            -   Done
7. Weather      -   Done            -   Done
8. Autos        -   Done            -   Done
9. Future       -   Done            -   Done
10. Earth       -   Done            -   Done
"""

Author.objects.all().delete()
Category.objects.all().delete()
Article.objects.all().delete()


def get_category(response, link):
    """get and return story's category from its url"""

    return response.urljoin(link).split("/")[3]


def add_slash_if_not(url):
    """Add forward slash at the end of url if not present
       It is used to get the desired behaviour from urljoin()
       function. urljoin() function replace last path component
       of our base url with our provided relative url if there
       is no forward slash at the end of base url. So, if our
       base url is https://bbc.com/earth/world and our relative
       url is abc. urljoin('https://bbc.com/earth/world', 'abc')
       would return https://bbc.com/earth/abc which we cetainly
       do not want. So, if we append forward slash '/' at the end
       of our base url if it is not already there we can get our
       desired result. urljoin('https://bbc.com/earth/world/', 'abc').
       Note the forward slash at the end of first argument to urljoin.
       It would return https://bbc.com/earth/world/abc
    """

    if url[-1] != '/':
        return url + '/'
    return url


class NewsSpider(scrapy.Spider):
    """
        parse() will parse the main homepage and gets categories link
        and forward it to parse_category() function

        parse_category() will parse categories page and gets
        all article link and forward it to parse_article() function.
        It also detects if there are more than one page then it follow
        that page and pass it to parse_category()

        parse_article() will parse the article page and extract
        article title, article published/last updated date, article body
        and article thumbnail image link.
    """

    name = "news_spider"
    start_urls = ['https://www.bbc.com/']

    def parse(self, response):
        """ Parses the homepage to get categories links
            and issue a response.follow() to download the category
            pages and parse them with parse_category() function """

        categories_links = response.xpath("""
                                            //div[@id='orb-footer']//div[@class='orb-footer-primary-links']
                                            //ul//li//a/@href
                                          """).extract()

        for link in categories_links:
            final_url = requests.request('HEAD', response.urljoin(link)).url
            # yield {'link':link}
            yield response.follow(final_url, callback=self.parse_category,
                                  meta={'follow_next': True}
                                  )

    def parse_category(self, response):
        """Parse category page for article links and issue request to
           download them and parse them with parse_article() and if there
           are more than one pages of the category; issue a response.follow()
           to parse the next page of category too to get article links"""

        url = urljoin(add_slash_if_not(response.url), '{page_no}')
        # yield {'link':response.url, 'url':url}
        # return 1
        article_links = []
        if b"itemsPerPage" in response.body:
            iterable = []
            if response.meta['follow_next']:
                iterable = range(2, 6)

            article_links = response.xpath("""//a[h3[@class='promo-unit-title']
                                                  and 
                                                  contains(
                                                  @data-cs-id, 'story-promo-link')]
                                                  /@href""").extract()

            for i in iterable:
                # yield {'next':url.format(page_no=i)}
                yield response.follow(url.format(page_no=i), callback=self.parse_category,
                                      meta={'follow_next': False, 'url': url}
                                      )

        elif response.url == 'https://www.bbc.com/weather':
            article_links = response.xpath(
                "//a[h3[contains(@class, 'title')]]/@href").extract()

        elif response.url == 'https://www.bbc.com/sport':
            article_links = response.xpath("""//article//
                                              a[span[contains(@class, 'title-text')]]
                                              /@href""").extract()

        elif response.url == 'https://www.bbc.com/news':
            article_links = response.xpath("""//a[contains(@class,'gs-c-promo-heading')
                                                  and
                                                  contains(@href, '/news/')]/@href""").extract()

        else:
            print("Meow Meow", response.url)

        for link in article_links:
            yield {'link': link}
            yield response.follow(link, callback=self.parse_article,
                                  meta={'category': get_category(
                                      response, link)}
                                  )

    def parse_article(self, response):
        """ Parses the given article to obtain article title,
            author, date on which article is published, articles's
            body and its category """

        article_title = ''
        article_author = ''
        article_date = ''
        article_body = ''
        article_category = response.meta['category']
        if article_category in ['travel', 'capital', 'culture', 'autos', 'future', 'earth']:
            # pass
            article_body = " ".join(response.xpath("""//div[@class='body-content']
                                                     //p[not(@class) and not(ancestor::blockquote)]
                                                     /text()""").extract())
            # article_body = replace_escape_chars(remove_tags(article_body))

            article_title = response.xpath(
                "//h1[@class='primary-heading']/text()").extract_first()

            article_author = response.xpath("""//li[contains(@class,'source-attribution-author')]
                                               /span/text()""").extract_first()

            article_date = response.xpath("""//span[contains(@class, 'publication-date')]
                                             /text()""").extract_first()

        elif article_category == 'weather':
            article_body = " ".join(response.xpath("""//div[contains(@class, 'feature-body')]
                                                      /p/text()""").extract())

            article_title = response.xpath("""//h1[contains(@class, 'header__title')]
                                              /text()""").extract_first()

            article_date = response.xpath("""//span[contains(@class, 'header__duration')]
                                             /b/text()""").extract_first()

        elif article_category == 'news':
            article_body = " ".join(response.xpath("""//div[@property='articleBody']
                                                     //*[self::p or self::h2]
                                                     /descendant-or-self::*/text()""").extract())

            article_title = response.xpath("""//div[@class='story-body']
                                              /h1[@class='story-body__h1']
                                              /text()""").extract_first()

            article_author = response.xpath(
                "//span[@class='byline__name']/text()").extract_first()

            article_date = response.xpath("""//div[contains(@class, 'date')
                                               and
                                               ancestor::div[@class='story-body']]
                                               /@data-datetime""").extract_first()

        elif article_category == 'sport':
            article_body = " ".join(response.xpath("""//div[@id='story-body']
                                                      /p/descendant::text()""").extract())

            article_title = response.xpath("""//article/h1[contains(@class, 'story-headline')]
                                              /text()""").extract_first()

            article_date = response.xpath("""//div[@class='story-info__list']
                                            //time/text()""").extract_first()

        else:
            print("Unknown category", article_category)

        if article_author:
            article_author = article_author.replace("By ", "")
        Article.objects.abk_insert(article_title, article_category,
                                   article_author, article_date,
                                   article_body)

        # uncomment the following line if you want to save parsed articles in a file
        # yield {
        #             'title': article_title,
        #             'body': article_body,
        #             'date': article_date,
        #             'author': article_author,
        #             'category': article_category
        #     }
