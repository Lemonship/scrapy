# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsspiderItem(scrapy.Item):
    date = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    link = scrapy.Field()
    

