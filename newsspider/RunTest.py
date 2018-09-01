from scrapy import cmdline

name = 'Test'
cmd = 'scrapy crawl {0}'.format(name) 
cmdline.execute(cmd.split())