from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem


class FancySpider(CrawlSpider):

    name = 'fancy'
    allowed_domains = ['fancy.com', ]
    start_urls = ['http://fancy.com/vinta', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'vinta/fancyd/\d+', ),  # http://fancy.com/vinta/fancyd/1365620197
                restrict_xpaths=('//div[@id="content"]//div[contains(@class, "pagination")]', ),
                unique=True,
            ),
            follow=True,
        ),
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'things/\d+/\S+', ),  # http://fancy.com/things/392410187429841177/Lenny-Sandals-by-MIA
                restrict_xpaths=('//div[@id="content"]//ol[contains(@class, "stream")]', ),
                unique=True,
            ),
            callback='parse_item_detail',
        ),
    )

    def parse_item_detail(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """

        hxs = HtmlXPathSelector(response)

        item = PhotoItem()

        item['comment'] = hxs.select('//*[@id="content"]//figure//figcaption/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="content"]//span[contains(@class, "wrapper-fig-image")]//img/@src').extract()
        item['source_url'] = response.url

        return item
