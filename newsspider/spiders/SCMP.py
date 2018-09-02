# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from newsspider.spiders.NewsSitemapSpider import NewsSitemapSpider
from newsspider.items import NewsspiderItem
import re
import datetime

class SCMPSpider(NewsSitemapSpider):
    name = 'SCMP'
    sitemap_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    allowed_domains = ['www.scmp.com']
    # sitemap_urls = ['https://www.scmp.com/sitemap_news.xml']
    sitemap_urls = [
        'https://www.scmp.com/sitemap_news.xml',
        'https://www.scmp.com/sitemap_economy.xml',
        'https://www.scmp.com/sitemap_business.xml',
        'https://www.scmp.com/sitemap_property.xml'
        ]
    #sitemap_follow = ['/要聞/','/港聞/','/經濟/','/中國/','/國際/','/地產/','/兩岸/']
    # custom_settings = {
    #     'FEED_EXPORT_FIELDS' : ["date", "category", "link", "keywords", "title", "desc"],
    # }    
    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url, headers=self.sitemap_header, callback=self._parse_sitemap)


    def parse(self, response):     
        item = NewsspiderItem()


        title = response.xpath("//meta[@property='og:title']/@content").extract_first()

        # title = response.xpath('//title/text()').extract()[0]
        # title = title.split(' | ')
         
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
