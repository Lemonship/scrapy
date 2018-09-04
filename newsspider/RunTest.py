from scrapy import cmdline

name = ['Test','Mingpao','Theguardian','Nytimes','SCMP']

cmd = 'scrapy crawl {0}'.format(name[0]) 
cmdline.execute(cmd.split())