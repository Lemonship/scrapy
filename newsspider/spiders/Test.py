# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime

class TestSpider(NewsSitemapSpider):
    name = 'Test'
    allowed_domains = ['www.theguardian.com']
    #start_urls = ['https://www.theguardian.com/australia-news/2018/aug/28/julie-bishop-to-remain-an-mp-but-keeps-future-options-open']
    sitemap_urls = ['https://www.theguardian.com/sitemaps/news.xml']
    #sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    custom_settings = {
        'FEED_EXPORT_FIELDS' : ["date", "category", "link", "keywords", "title", "desc"],
    }    

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath('//title/text()').extract()[0]
        title = title.split(' | ')
        date = re.search(r'(\d{4})/([a-z]{3})/(\d{2})',response.url)
        date = ''.join(date.groups())
        date = datetime.datetime.strptime(date,'%Y%b%d')
        date = date.strftime('%Y%m%d')
        item['date'] = date
        item['category'] = title[1]
        item['title'] = title[0]
        item['desc'] = ''.join(response.xpath('//p/text()').extract())
        item['link'] =  response.url
        item['keywords'] = response.meta['keywords']
        yield item 
