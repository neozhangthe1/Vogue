from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from crawler.crawler.items import PhotoItem


class MAFFASHIONSpider(CrawlSpider):

    name = 'madamejulietta'
    allowed_domains = ['madamejulietta.blogspot.tw', ]
    start_urls = ['http://madamejulietta.blogspot.tw/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://atlantic-pacific.blogspot.tw/search?updated-max=2013-10-28T16:40:00-04:00&max-results=4
                restrict_xpaths=('//*[@id="blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+.html', ),  # http://atlantic-pacific.blogspot.tw/2013/10/guest-bartender-baublebar-x-bee.html
                restrict_xpaths=('//*[@id="Blog1"]/div[1]', ),
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

        sel = Selector(response, type='html')

        item = PhotoItem()
        item['comment'] = sel.xpath('//title/text()').extract()
        item['image_urls'] = sel.xpath('//*[@id="Blog1"]/div[1]/div/div/div/div[1]//img/@src').extract()
        item['source_url'] = response.url

        return item
