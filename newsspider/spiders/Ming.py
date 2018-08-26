# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.spiders import SitemapSpider
from newsspider.items import NewsspiderItem
import re


class MingSpider(SitemapSpider):
    name = 'Ming'
    allowed_domains = ['news.mingpao.com']
    sitemap_urls = ['https://news.mingpao.com/robots.txt']
    #sitemap_follow = ['/要聞','/港聞','/經濟','/中國','/國際','/地產','/兩岸']

    def parse(self, response):
        # # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)        
        #filename = 'MingData.json'
        item = NewsspiderItem()

        #with open(filename, 'wb') as f:
        title = response.xpath('//title/text()').extract()[0]
        title = re.split(' - ',title)
        item['date'] = title[1]
        item['category'] = title[2]
        item['title'] = title[0]
        item['desc'] = response.xpath('//p/text()').extract()
        item['link'] =  response.url
        yield item 

        # print(item)
            #f.write(item)

