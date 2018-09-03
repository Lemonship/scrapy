from scrapy import cmdline

name = 'Theguardian'
cmd = 'scrapy crawl {0}'.format(name) 
cmdline.execute(cmd.split())