import scrapy
from scrapy.utils.response import open_in_browser

"""
TODO
Category Name   - Digital Data
1. Travel       -   True
2. News         -   False
3. Capital      -   True
4. Arts         -   False   - HTML data in response to ajax request
5. Sport        -   False   - //article//a[span[contains(@class, 'title-text')]]
6. Culture      -   True
7. Weather      -   False   - //a[h3[contains(@class, 'title')]]
8. Autos        -   True
9. Food         -   False
10. Future      -   True
11. Earth       -   False
"""


from w3lib.html import remove_tags, replace_escape_chars, replace_tags

class NewsSpider(scrapy.Spider):
    """
        parse() will parse the main homepage and gets categories link
        and forward it to parse_categories() function

        parse_categories() will parse categories page and gets
        all article link and forward it to parse_article() function

        parse_article() will parse the article page and extract
        article title, article published/last updated date, article body
        and article thumbnail image link.
    """

    name = "news_spider"
    start_urls = ['https://www.bbc.com']

    def parse(self, response):
        categories_links = response.css("#orb-footer div.orb-footer-primary-links")
        categories_links = categories_links.css("ul li a::attr(href)").extract()

        for link in categories_links:
            yield response.follow(link, callback=self.parse_categories)
    

    def parse_categories(self, response):
        article_links = response.xpath("//a[h3[@class='promo-unit-title']]/@href").extract()
        most_popular_items = response.xpath("//a[@class='most-popular-item-lining']/@href").extract()
        article_links = article_links + most_popular_items
        for link in article_links:
            yield {'link': link}
            # yield response.follow(link, callback=self.parse_article)


    def parse_article(self, response):
        article_body = " ".join(response.css(".post_content p").extract())
        article_body = replace_escape_chars(remove_tags(article_body))
        
        article_title = response.css("#main-heading .page-title::text").extract_first()
        
        article_date = response.css(".post-info .post_date").extract_first().encode('ascii', 'ignore')
        article_date = replace_escape_chars(replace_tags(article_date, ' '))
        article_date = article_date.replace("Last Updated On", "").strip()  # datetime.strptime(d, "%d %B,%Y %I:%M %p")

        yield {
                'title': article_title,
                'body': article_body,
                'date': article_date
              }