from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem



class PinterestSpider(CrawlSpider):

    name = 'pinterest'
    allowed_domains = ['www.pinterest.com', ]
    start_urls = ['http://www.pinterest.com/vintalines/likes/', ]

    rules = (
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'pin/\d+/$', ),  # http://pinterest.com/pin/128141551870912604/
                unique=True,
            ),
            callback='parse_pin_detail',
        ),
    )

    def parse_pin_detail(self, response):
        hxs = HtmlXPathSelector(response)

        item = PhotoItem()

        item['comment'] = hxs.select('//title/text()').extract()

        urls_1 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//img/@src').extract()
        urls_2 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//a/@href').extract()
        item['image_urls'] = urls_1 + urls_2

        item['source_url'] = response.url

        return item
