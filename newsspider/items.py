# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsspiderItem(scrapy.Item):
    publication_date = scrapy.Field()
    maincategory = scrapy.Field()
    subcategory = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    link = scrapy.Field()
    keywords = scrapy.Field()
    
class NewsSitemapItem(scrapy.Item):
    loc = scrapy.Field()
    publication_name = scrapy.Field()
    language = scrapy.Field()
    publication_date = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
