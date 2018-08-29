import lxml.etree
from six.moves.urllib.parse import urljoin
import re

class Sitemap(object):
    """Class to parse Sitemap (type=urlset) and Sitemap Index
    (type=sitemapindex) files"""

    def __init__(self, xmltext):
        xmlp = lxml.etree.XMLParser(recover=True, remove_comments=True, resolve_entities=False)
        self._root = lxml.etree.fromstring(xmltext, parser=xmlp)
        rt = self._root.tag
        self.type = self._root.tag.split('}', 1)[1] if '}' in rt else rt

    def __iter__(self):
        for elem in self._root.getchildren():
            d = {}
            for el in elem.getchildren():
                tag = el.tag
                name, nspace = gettagname(tag)
                if name == 'link':
                    if 'href' in el.attrib:
                        d.setdefault('alternate', []).append(el.get('href'))
                elif name == 'news' and 'http://www.google.com/schemas/sitemap-news/' in nspace:
                    d[name] = getobjectcontent(el)
                else:
                    d[name] = el.text.strip() if el.text else ''

            if 'loc' in d:
                yield d

def getobjectcontent(item):
    itemlist = {}
    for subitem in item.getchildren():
        name, _ = gettagname(subitem.tag)
        if len(subitem.getchildren()) > 0:
            itemlist[name] = getobjectcontent(subitem)
        elif subitem.text is not None:
            itemlist[name] = subitem.text.strip()
        else:
            itemlist[name] = ''
    return itemlist


def gettagname(tag):
    results = re.search(r'\{(\S*)\}(\S*)',tag)
    if results is None:
        return tag, ''
    else:
        return results.group(2), results.group(1) 

