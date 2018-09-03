# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime
from dateutil import parser

class MingpaoSpider(NewsSitemapSpider):
    name = 'Mingpao'
    allowed_domains = ['news.mingpao.com']
    sitemap_urls = ['https://news.mingpao.com/sitemap.xml']
    sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    def _index_filter(self, item):
        date = item['publication_date']
        date = parser.parse(date).date()
        return (date >= (datetime.datetime.today() + datetime.timedelta(days=-3)).date())

    def parse(self, response):     
        item = NewsspiderItem()
        title = response.xpath('//title/text()').extract()[0]
        # title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        title = re.split(' - ',title)
        article = ''.join(response.xpath('//p/text()').extract())
        article = article.replace('\n','')
        item['publication_date'] = title[1]
        item['maincategory'] = title[2]
        item['subcategory'] = title[3]
        item['title'] = title[0]
        item['desc'] = article
        item['link'] =  response.url
        item['keywords'] = response.meta['keywords']        
        yield item 
