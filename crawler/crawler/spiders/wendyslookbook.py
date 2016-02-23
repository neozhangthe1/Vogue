from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem


class WendysLookbookSpider(CrawlSpider):

    name = 'wendyslookbook'
    allowed_domains = ['www.wendyslookbook.com', ]
    start_urls = ['http://www.wendyslookbook.com/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'page/\d+/', ),  # http://www.wendyslookbook.com/page/2/
                restrict_xpaths=('//*[@id="coreContent"]/div[6]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+/', ),  # http://www.wendyslookbook.com/2013/06/pick-me-up-striped-sequin-tulle-skirt/
                restrict_xpaths=('//*[@id="coreContent"]', ),
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
        item['image_urls'] = hxs.select('//*[@id="coreContent"]/div[1]/div[1]/div//img/@src').extract()
        item['source_url'] = response.url

        return item
