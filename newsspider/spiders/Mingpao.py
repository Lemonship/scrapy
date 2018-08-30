# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re


class MingpaoSpider(NewsSitemapSpider):
    name = 'Mingpao'
    allowed_domains = ['news.mingpao.com']
    sitemap_urls = ['https://news.mingpao.com/robots.txt']
    sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    # custom_settings = {
    #     'FEED_EXPORT_FIELDS' : ["date", "category", "link", "title", "desc"],
    # }    

    def parse(self, response):     
        item = NewsspiderItem()
        title = response.xpath('//title/text()').extract()[0]
        title = re.split(' - ',title)
        item['date'] = title[1]
        item['category'] = title[2]
        item['title'] = title[0]
        item['desc'] = response.xpath('//p/text()').extract()[0]
        item['link'] =  response.url
        item['keywords'] = response.meta['keywords']        
        yield item 


class MingTestSpider(Spider):
    name = 'MingTest'
    allowed_domains = ['news.mingpao.com']
    start_urls = ['https://news.mingpao.com/pns/dailynews/web_tc/article/20180827/s00002/1535307044467']
    # sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    # custom_settings = {
    #     # 'FEED_EXPORT_FIELDS' : ["date", "category", "link", "title", "desc"],
    # }    

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath('//title/text()').extract()[0]
        title = re.split(' - ',title)
        item['date'] = title[1]
        item['category'] = title[2]
        item['title'] = title[0]
        item['desc'] = response.xpath('//p/text()').extract()[0]
        item['link'] =  response.url
        yield item 

