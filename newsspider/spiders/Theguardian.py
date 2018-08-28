# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.spiders import SitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime

class TheguardianSpider(Spider):
    name = 'Theguardian'
    allowed_domains = ['www.theguardian.com']
    sitemap_urls = ['https://www.theguardian.com/sitemaps/news.xml']
    #sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    # custom_settings = {
    #     'FEED_EXPORT_FIELDS' : ["date", "category", "link", "title", "desc"],
    # }    

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath('//title/text()').extract()[0]
        title = title.split(' | ')
        url = response.url.split('/')
        date = url[4] + url[5] + url[6]
        date = datetime.datetime.strptime(date,'%Y%b%d')
        date = date.strftime('%Y%m%d')
        item['date'] = date
        item['category'] = title[1]
        item['title'] = title[0]
        item['desc'] = response.xpath('//p/text()').extract()[0]
        item['link'] =  response.url
        yield item 
