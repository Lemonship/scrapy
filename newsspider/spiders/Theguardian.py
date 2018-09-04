# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime
from dateutil import parser

class TheguardianSpider(NewsSitemapSpider):
    name = 'Theguardian'
    allowed_domains = ['www.theguardian.com']
    sitemap_urls = ['https://www.theguardian.com/sitemaps/news.xml']

    def __init__(self, datestart = None, dateend= None, *a, **kw):
        super(TheguardianSpider, self).__init__(*a, **kw)
        if datestart is not None:
            self.datestart = datetime.datetime.strptime(datestart,'%Y%m%d').date()
        else:
            self.datestart = (datetime.datetime.now() + datetime.timedelta(days=-3)).date()
        if dateend is not None:
            self.dateend = datetime.datetime.strptime(dateend,'%Y%m%d').date()
        else:
            self.dateend = (self.datestart + datetime.timedelta(days=3)).date

    def _index_filter(self, item):
        date = item['publication_date']
        date = parser.parse(date).date()
        result =  (self.datestart <= date <= self.dateend)
        return result

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        MainCat = response.xpath("//meta[@property='article:section']/@content").extract_first()
        SubCat = MainCat
        article = ''.join(response.xpath('//p/text()').extract())
        article = article.replace('\n','')
        date = re.search(r'(\d{4})/([a-z]{3})/(\d{2})',response.url)
        date = ''.join(date.groups())
        date = datetime.datetime.strptime(date,'%Y%b%d')
        date = date.strftime('%Y%m%d')
        keywords = response.meta['keywords']

        item['publication_date'] = date
        item['maincategory'] = MainCat
        item['subcategory'] = SubCat
        item['title'] = title
        item['desc'] = article
        item['link'] =  response.url
        item['keywords'] = keywords
        yield item 

