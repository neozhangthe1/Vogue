from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem


class IvoryLaneSpider(CrawlSpider):

    name = 'theivorylane'
    allowed_domains = ['theivorylane.com', ]
    start_urls = ['http://www.theivorylane.com/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://www.theivorylane.com/search?updated-max=2013-11-22T05:01:00-08:00&max-results=4
                restrict_xpaths=('//*[@id="blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+.html', ),  # http://www.theivorylane.com/2013/11/loft-holiday.html
                restrict_xpaths=('//*[@id="Blog1"]/div[contains(@class, "blog-posts")]', ),
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
        item['image_urls'] = hxs.select('//*[@id="Blog1"]//div[contains(@class, "post")]//div[contains(@class, "post-body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
