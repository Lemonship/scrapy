from scrapy import cmdline

""" 
from scrapy.crawler import CrawlerProcess
import time

from apscheduler.schedulers.background import BackgroundScheduler
def task():
    # 你的spider启动命令
    process = CrawlerProcess(get_project_settings())

    process.crawl(PostSpider)
    process.start() # the script will block here until the crawling is finished
    # pass

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # 每20分钟执行一次
    scheduler.add_job(task, 'cron', minute="*/20")
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
     """


name = 'Mingpao'
# cmd = 'scrapy crawl {0} -o Ming.json'.format(name) 
cmd = 'scrapy crawl {0}'.format(name) 
cmdline.execute(cmd.split())
