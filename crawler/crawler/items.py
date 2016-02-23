# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PhotoItem(Item):
    comment = Field()
    source_url = Field()
    image_urls = Field()
    images = Field()
