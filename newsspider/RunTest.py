from scrapy import cmdline

name = 'SCMP'
cmd = 'scrapy crawl {0}'.format(name) 
cmdline.execute(cmd.split())