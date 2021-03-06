# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime
from dateutil import parser

class SCMPSpider(NewsSitemapSpider):
    name = 'SCMP'
    sitemap_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    allowed_domains = ['www.scmp.com']
    sitemap_urls = [
        'https://www.scmp.com/sitemap_news.xml',
        'https://www.scmp.com/sitemap_economy.xml',
        'https://www.scmp.com/sitemap_business.xml',
        'https://www.scmp.com/sitemap_property.xml'
        ]

    def __init__(self, datestart = None, dateend= None, *a, **kw):
        super(SCMPSpider, self).__init__(*a, **kw)
        if datestart is not None:
            self.datestart = datetime.datetime.strptime(datestart,'%Y%m%d').date()
        else:
            self.datestart = (datetime.datetime.now() + datetime.timedelta(days=-3)).date()
        if dateend is not None:
            self.dateend = datetime.datetime.strptime(dateend,'%Y%m%d').date()
        else:
            self.dateend = (self.datestart + datetime.timedelta(days=3)).date

    def _index_filter(self, item):
        changefreq = item['changefreq']
        date = item['lastmod']
        # date = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%MZ')
        date = parser.parse(date).date()
        result = (changefreq == 'daily') and (self.datestart <= date <= self.dateend)
        return result

    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, headers=self.sitemap_header, callback=self._parse_sitemap)


    def parse(self, response):     
        item = NewsspiderItem()
        URLInfo = re.search(r'/(?P<MainCat>[\w-]+)/(?P<SubCat>[\w-]+)/article/',response.url)
        if URLInfo is None:
            URLInfo = re.search(r'/(?P<MainCat>[\w-]+)/article/',response.url)
            MainCat = URLInfo.group('MainCat')
            SubCat = MainCat
        else:
            MainCat = URLInfo.group('MainCat')
            SubCat = URLInfo.group('SubCat')
        title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        date = response.xpath("//meta[@property='article:published_time']/@content").extract_first()
        date = datetime.datetime.strptime(date.replace(':',''),'%Y-%m-%dT%H%M%S%z')
        date = date.strftime('%Y%m%d')
        keywords = response.xpath("//meta[@name='keywords']/@content").extract_first()
        # date = ''.join(URLInfo.group('YYYY','MM','dd'))
        
        # date = datetime.datetime.strptime(date,'%Y%b%d')
        # date = date.strftime('%Y%m%d')
        
        item['publication_date'] = date
        item['maincategory'] = MainCat
        item['subcategory'] = SubCat
        item['title'] = title
        item['desc'] = ''.join(response.xpath("//div[@class='pane-content']/p/text()").extract())
        item['link'] =  response.url
        item['keywords'] = keywords
        yield item 
