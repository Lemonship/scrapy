from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import time

# from apscheduler.schedulers.background import BackgroundScheduler

RUN_SPIDER_NAMES = ['Mingpao','Theguardian']

def spider_start():
    print 'spider_start called'
    receiver = Receiver(len(MY_SPIDER_NAMES))
    for spider_name in MY_SPIDER_NAMES:
        cls = get_class(MY_SPIDER_MODULES.get(spider_name))
        spider = cls()
        set_crawler(spider, receiver)
    reactor.run()

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

