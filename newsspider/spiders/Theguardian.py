# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime

class TheguardianSpider(NewsSitemapSpider):
    name = 'Theguardian'
    allowed_domains = ['www.theguardian.com']
    sitemap_urls = ['https://www.theguardian.com/sitemaps/news.xml']
    #sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    # custom_settings = {
    #     'FEED_EXPORT_FIELDS' : ["date", "category", "link", "keywords", "title", "desc"],
    # }

    def parse(self, response):     
        item = NewsspiderItem()

        title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        category = response.xpath("//meta[@property='article:section']/@content").extract_first()
        
        # title = response.xpath('//title/text()').extract()[0]
        # title = title.split(' | ')
        article = ''.join(response.xpath('//p/text()').extract())
        article = article.replace('\n','')
        date = re.search(r'(\d{4})/([a-z]{3})/(\d{2})',response.url)
        date = ''.join(date.groups())
        date = datetime.datetime.strptime(date,'%Y%b%d')
        date = date.strftime('%Y%m%d')
        item['publication_date'] = date
        item['maincategory'] = category
        item['subcategory'] = category
        item['title'] = title
        item['desc'] = article
        item['link'] =  response.url
        item['keywords'] = response.meta['keywords']
        yield item 
