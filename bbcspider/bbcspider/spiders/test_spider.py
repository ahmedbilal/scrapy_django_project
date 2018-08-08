import scrapy
from scrapy.utils.response import open_in_browser

"""
TODO
Category Name   - Digital Data  -   Link Collection -   Data Extraction
1. Travel       -   True        -   Done            -   Done
2. News         -   False       -   Not Done        
3. Capital      -   True        -   Done            -   Done
4. Arts         -   False       -   Not Done                                HTML data in response to ajax request
5. Sport        -   False       -   Not Done                                //article//a[span[contains(@class, 'title-text')]]
6. Culture      -   True        -   Done            -   Done
7. Weather      -   False       -   Done            -   Done                                   //a[h3[contains(@class, 'title')]]
8. Autos        -   True        -   Done            -   Done
9. Food         -   False       -   Not Done
10. Future      -   True        -   Done            -   Done
11. Earth       -   True        -   Not Good
"""


from w3lib.html import remove_tags, replace_escape_chars, replace_tags

class NewsSpider(scrapy.Spider):
    """
        parse() will parse the main homepage and gets categories link
        and forward it to parse_categories() function

        parse_categories() will parse categories page and gets
        all article link and forward it to parse_article() function.
        It also detects if there are more than one page then it follow
        that page and pass it to parse_categories()

        parse_article() will parse the article page and extract
        article title, article published/last updated date, article body
        and article thumbnail image link.
    """

    name = "test_spider"
    start_urls = ['https://www.bbc.com/']

    def parse(self, response):
        categories_links = response.xpath("//div[@id='orb-footer']//div[@class='orb-footer-primary-links']//ul//li//a/@href").extract()

        for link in categories_links:
            #yield {'link':link}
            # yield {'link':response.urljoin(link)}
            yield response.follow(link, callback=self.parse_categories,
                                  meta={
                                        'follow_next':True,
                                        'url':"{url}{{page_no}}".format(url=link),
                                    }
                                 )
    

    def parse_categories(self, response):
        if b"itemsPerPage" in response.body:
            url = response.meta['url']
            iterable = []
            if response.meta['follow_next']:
                iterable = range(2, 11)
            
            article_links = response.xpath("//a[h3[@class='promo-unit-title'] and contains(@data-cs-id, 'story-promo-link')]/@href").extract()
            for link in article_links:
                yield {'category':response.urljoin(link).split("/")[3]}
                # yield response.follow(link, callback=self.parse_article, meta={'category':'default'})

            for i in iterable:
                yield response.follow(url.format(page_no=i), callback=self.parse_categories,
                                        meta={
                                                'follow_next':False,
                                                'url':url,
                                            }
                                        )
        
        elif response.url == 'https://www.bbc.com/weather':
            article_links = response.xpath("//a[h3[contains(@class, 'title')]]/@href").extract()
            for link in article_links:
                yield {'category':response.urljoin(link).split("/")[3]}
                # yield response.follow(link, callback=self.parse_article, meta={'category':'weather'})
        
        else:
            print("Meow Meow", response.url)


    def parse_article(self, response):
        if response.meta['category'] == 'default':
            article_body = " ".join(response.xpath("//div[@class='body-content']//p[not(@class) and not(ancestor::blockquote)]/text()").extract())
            #article_body = replace_escape_chars(remove_tags(article_body))
            
            article_title = response.xpath("//h1[@class='primary-heading']/text()").extract_first()
            article_author = response.xpath("//li[contains(@class,'source-attribution-author')]/span/text()").extract_first()
            article_date = response.xpath("//span[contains(@class, 'publication-date')]/text()").extract_first()

            yield {
                    'title': article_title,
                    'body': article_body,
                    'date': article_date,
                    'author': article_author,
                    'url':response.url
                }
        elif response.meta['category'] == 'weather':
            article_body = " ".join(response.xpath("//div[contains(@class, 'feature-body')]/p/text()").extract())
            article_title = response.xpath("//h1[contains(@class, 'header__title')]/text()").extract_first()
            article_date = response.xpath("//span[contains(@class, 'header__duration')]/b/text()").extract_first()

            yield {
                    'title': article_title,
                    'body': article_body,
                    'date': article_date,
                    'url':response.url
                }
        elif response.meta['category'] == 'news':
            pass