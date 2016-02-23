from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from crawler.crawler.items import PhotoItem



class RozaliaFashionSpider(CrawlSpider):

    name = 'rozaliafashion'
    allowed_domains = ['rozaliafashion.blogspot.co.uk', ]
    start_urls = ['http://rozaliafashion.blogspot.co.uk/', ]

    rules = (
        # find next page
        Rule(
            SgmlLinkExtractor(
                allow=(r'search\?updated-max=', ),  # http://rozaliafashion.blogspot.co.uk/search?updated-max=2014-06-14T01:16:00-07:00&max-results=5
                restrict_xpaths=('//*[@id="blog-pager-older-link"]', ),
                unique=True,
            ),
            follow=True,
        ),

        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'\d+/\d+/[\w-]+.html', ),  # http://rozaliafashion.blogspot.co.uk/2014/06/bajmi.html
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

        sel = Selector(response, type='html')

        item = PhotoItem()
        item['comment'] = sel.xpath('//title/text()').extract()
        item['image_urls'] = sel.xpath('//div[contains(@class, "post")]//div[contains(@class, "post-body")]//img/@src').extract()
        item['source_url'] = response.url

        return item
