from scrapy import cmdline


name = 'Ming'
cmd = 'scrapy crawl {0} -o Ming.json'.format(name) 
cmdline.execute(cmd.split())