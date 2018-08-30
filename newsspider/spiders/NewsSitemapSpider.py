# import re
import logging
# import six

from scrapy.spiders import Spider, SitemapSpider
from scrapy.http import Request, XmlResponse
from scrapy.utils.sitemap import sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, gzip_magic_number
from newsspider.items import NewsSitemapItem
from newsspider.util.deepsitemap import Sitemap

logger = logging.getLogger(__name__)


class NewsSitemapSpider(SitemapSpider):          
    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap)
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
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                if 'http://www.google.com/schemas/sitemap-news/' in s._root.nsmap['news']:
                    for news in iternews(s, self.sitemap_alternate_links):
                        for r, c in self._cbs:
                            if r.search(news['loc']):
                                yield Request(news['loc'], callback=c, meta=news)
                                break
                else:
                    for loc in iterloc(s, self.sitemap_alternate_links):
                        for r, c in self._cbs:
                            if r.search(loc):
                                yield Request(loc, callback=c)
                                break

# def regex(x):
#     if isinstance(x, six.string_types):
#         return re.compile(x)
#     return x
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

def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l
