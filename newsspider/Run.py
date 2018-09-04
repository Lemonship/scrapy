
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import time

# from scrapy import cmdline
# from apscheduler.schedulers.background import BackgroundScheduler

RUN_SPIDER_NAMES = ['Mingpao','Theguardian','Nytimes','SCMP']

# RUN_SPIDER_NAMES = ['Mingpao']
DATESTART = '20180801'
DATEEND = '20180831'
# for spidername in RUN_SPIDER_NAMES:
#     cmd = 'scrapy crawl {0}'.format(spidername) 
#     cmdline.execute(cmd.split())

def spider_start():
    print('spider_start called')
    process = CrawlerProcess(get_project_settings())
    for spider_name in RUN_SPIDER_NAMES:
        spider_name = spider_name
        process.crawl(spider_name, datestart = DATESTART, dateend = DATEEND)
        print('{} called'.format(spider_name))
    process.start() 

spider_start()
""" 

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