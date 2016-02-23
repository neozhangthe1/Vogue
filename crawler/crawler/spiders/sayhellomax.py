from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem



class SayHelloMaxSpider(CrawlSpider):

    name = 'sayhellomax'
    allowed_domains = ['sayhellomax.com', ]
    start_urls = ['http://www.sayhellomax.com/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://www.sayhellomax.com/search?updated-max=2013-10-21T08:00:00-07:00&max-results=10
                restrict_xpaths=('//a[@id="Blog1_blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+.html', ),  # http://www.sayhellomax.com/2013/11/bundled.html
                restrict_xpaths=('//div[@id="Blog1"]//div[contains(@class, "blog-posts")]', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = PhotoItem()

        item['comment'] = hxs.select('//title/text()').extract()
        item['image_urls'] = hxs.select('//div[contains(@class, "post")]//div[contains(@class, "post-body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
