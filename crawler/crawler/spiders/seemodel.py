# coding: utf-8

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest

from crawler.crawler.items import PhotoItem


class SeeModelSpider(CrawlSpider):
    name = 'seemodel'
    allowed_domains = ['www.seemodel.com', ]
    login_page = 'http://www.seemodel.com/member.php?mod=logging&action=login'
    start_urls = [
        'http://www.seemodel.com/forum.php?mod=forumdisplay&fid=41&filter=heat&orderby=heats',
        'http://www.seemodel.com/forum.php?mod=forumdisplay&fid=42&filter=heat&orderby=heats',
    ]

    rules = (
        Rule(
            SgmlLinkExtractor(allow=r'forum\.php\?mod=viewthread&tid=\d+'),
            callback='parse_item',
            follow=False,
        ),
    )

    def start_requests(self):
        self.username = self.settings['SEEMODEL_USERNAME']
        self.password = self.settings['SEEMODEL_PASSWORD']

        yield Request(
            url=self.login_page,
            callback=self.login,
            dont_filter=True,
        )

    def login(self, response):
        return FormRequest.from_response(
            response,
            formname='login',
            formdata={
                'username': self.username,
                'password': self.password,
                'cookietime': 'on',
            },
            callback=self.check_login_response,
        )

    def check_login_response(self, response):
        """
        Check the response returned by a login request to see if we are
        successfully logged in.
        """

        if self.username not in response.body:
            self.log("Login failed")
            return

        self.log("Successfully logged in")

        return [Request(url=url, dont_filter=True) for url in self.start_urls]

    def parse_item(self, response):
        item = PhotoItem()
        item['comment'] = response.xpath('//*[@id="thread_subject"]/text()').extract()
        item['image_urls'] = response.xpath('//ignore_js_op//img/@zoomfile').extract()
        item['source_url'] = response.url

        return item
