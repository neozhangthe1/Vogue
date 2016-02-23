from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem



class SaucyGlossieSpider(CrawlSpider):

    name = 'saucyglossie'
    allowed_domains = ['www.saucyglossie.com', ]
    start_urls = ['http://www.saucyglossie.com/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'page/\d+/', ),  # http://www.saucyglossie.com/page/2/
                restrict_xpaths=('//*[@id="container_wrapper"]//div[contains(@class, "wp-pagenavi")]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'/[\w-]+/', ),  # http://www.saucyglossie.com/natures-neutrals/
                restrict_xpaths=('//*[@id="container_wrapper"]//div[contains(@class, "count_l")]', ),
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
        item['image_urls'] = hxs.select('//*[@id="container_wrapper"]//div[contains(@class, "contentwrap")]//img/@src').extract()
        item['source_url'] = response.url

        return item
