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
    allowed_domains = ['www.nytimes.com']
    sitemap_urls = ['https://www.nytimes.com/sitemaps/sitemap_news/sitemap.xml.gz']
    #sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    custom_settings = {
        'FEED_EXPORT_FIELDS' : ["date", "category", "link", "keywords", "title", "desc"],
    }    

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath('//title/text()').extract()[0]
        title = title.split(' | ')
        URLInfo = re.search(r'/(?P<YYYY>\d{4})/(?P<MM>\d{2})/(?P<dd>\d{2})/(?P<MainCat>\w*)/(?P<SubCat>\w*)/',response.url)
        date = ''.join(URLInfo.group('YYYY','MM','dd'))
        date = datetime.datetime.strptime(date,'%Y%b%d')
        date = date.strftime('%Y%m%d')
        
        item['date'] = date
        item['category'] = title[1]
        item['title'] = title[0]
        item['desc'] = ''.join(response.xpath('//p/text()').extract())
        item['link'] =  response.url
        item['keywords'] = response.meta['keywords']
        yield item 
