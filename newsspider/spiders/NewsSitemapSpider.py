import logging

from scrapy.spiders import Spider, SitemapSpider
from scrapy.http import Request, XmlResponse
from scrapy.utils.sitemap import sitemap_urls_from_robots
from newsspider.items import NewsSitemapItem
from newsspider.util.deepsitemap import Sitemap

logger = logging.getLogger(__name__)


class NewsSitemapSpider(SitemapSpider):
    sitemap_header = {}        
    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap,headers = self.sitemap_header)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning("Ignoring invalid sitemap: %(response)s",
                                {'response': response}, extra={'spider': self})
                return

            s = Sitemap(body)
            if s.type == 'sitemapindex':
                for loc in iterloc(s, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap,headers = self.sitemap_header )
            elif s.type == 'urlset':
                if 'news' in s._root.nsmap and 'http://www.google.com/schemas/sitemap-news/' in s._root.nsmap['news']:
                    for news in iternews(s, self.sitemap_alternate_links):
                        if self._index_filter(news):
                            for r, c in self._cbs:
                                if r.search(news['loc']):
                                    yield Request(news['loc'], callback=c, meta=news, headers = self.sitemap_header)
                                    break
                else:
                    for item in iteritem(s):
                        if self._index_filter(item):
                            for r, c in self._cbs:
                                if r.search(item['loc']):
                                    yield Request(item['loc'], callback=c, meta=item, headers = self.sitemap_header)
                                    break
    def _index_filter(self,item):
        return True
def iternews(it, alt=False):
    for d in it:
        news = NewsSitemapItem()
        news['loc'] = d['loc']
        news['publication_name'] = d['news']['publication']['name']
        news['language'] = d['news']['publication']['language']
        news['publication_date'] = d['news']['publication_date']
        news['title'] = d['news']['title']
        news['keywords'] = d['news']['keywords']
        yield news

        # # Also consider alternate URLs (xhtml:link rel="alternate")
        # if alt and 'alternate' in d:
        #     for l in d['alternate']:
        #         yield l

def iteritem(it):
    for d in it:
        yield d

def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l
