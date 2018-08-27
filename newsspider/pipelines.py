# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import JsonLinesItemExporter


class JsonDatePipeline(object):
    
    # def process_item(self, item, spider):
    #     return item

    def open_spider(self, spider):
        self.export_item_date = {}

    def _exporter_for_item(self, item):
        date = item['date']
        if date not in self.export_item_date:
            f = open('ScrapyData/' + '{}.json'.format(date), 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.encoding = 'utf-8'
            exporter.encoder.ensure_ascii = False
            exporter.start_exporting()
            self.export_item_date[date] = exporter
        return self.export_item_date[date]
        
    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

    def close_spider(self, spider):
        for exporter in self.export_item_date.values():
            exporter.finish_exporting()
            exporter.file.close() 

# class JsonWithEncodingPipeline(object):
#     def open_spider(self, spider):        
#         self.filename = '%s_output.json' % spider.name
#         self.file = open('ScrapyData/' + self.filename, 'w', encoding='utf-8')

#     def close_spider(self, spider):
#         self.file.close()

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
#         self.file.write(line)
#         return item

