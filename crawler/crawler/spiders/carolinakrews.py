from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from crawler.crawler.items import PhotoItem



class CarolinaKrewsSpider(CrawlSpider):

    name = 'carolinakrews'
    allowed_domains = ['carolinakrews.blogspot.tw', ]
    start_urls = ['http://carolinakrews.blogspot.tw/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://carolinakrews.blogspot.tw/search?updated-max=2013-10-17T10:37:00-07:00&max-results=8
                restrict_xpaths=('//*[@id="Blog1_blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+.html', ),  # http://www.ohmyvogue.com/2013/08/nude-white.html
                restrict_xpaths=('//*[@id="Blog1"]/div[contains(@class, "blog-posts")]', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        hxs = HtmlXPathSelector(response)

        item = PhotoItem()
        item['comment'] = hxs.select('//title/text()').extract()
        item['image_urls'] = hxs.select('//*[@id="Blog1"]//div[contains(@class, "post-body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
