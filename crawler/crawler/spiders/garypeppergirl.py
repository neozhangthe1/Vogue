from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem



class GaryPepperSpider(CrawlSpider):

    name = 'garypeppergirl'
    allowed_domains = ['garypeppergirl.com', ]
    start_urls = ['http://garypeppergirl.com/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'page/\d+', ),  # http://garypeppergirl.com/page/3
                restrict_xpaths=('//*[@id="wrap"]//div[contains(@class, "pagination-gamma")]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+', ),  # http://garypeppergirl.com/2013/03/sixty
                restrict_xpaths=('//*[@id="posts"]//div[contains(@class, "post")]//div[contains(@class, "title")]', ),
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

        item['comment'] = hxs.select('//*[@id="post"]//div[contains(@class, "title")]//a/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="post"]//div[contains(@class, "media")]//img/@src').extract()
        item['source_url'] = response.url

        return item
