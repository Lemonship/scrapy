# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime
# from dateutil import parser

class TestSpider(NewsSitemapSpider):
    name = 'Test'
    sitemap_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    allowed_domains = ['www.theguardian.com']
    sitemap_urls = ['https://www.theguardian.com/sitemaps/news.xml']

    def _index_filter(self, item):
        date = item['publication_date']
        date = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ')
        if date > (datetime.datetime.now() + datetime.timedelta(days=-3)):
            return True
        else:
            return False

    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, headers=self.sitemap_header, callback=self._parse_sitemap)

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
