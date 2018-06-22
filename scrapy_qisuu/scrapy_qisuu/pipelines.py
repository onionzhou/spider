# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ScrapyQisuuPipeline(object):
    def __init__(self):
        self.file = open('book2.json','w')
    def open_spider(self,spider):
        pass
    def process_item(self, item,spider):
        if item :
            #中文无法写入？？？
            # content = json.dumps(dict(item),ensure_ascii=False) + "\n"
            content = json.dumps(dict(item)) + "\n"
            self.file.write(content)
        return item
    def close_spider(self,spider):
        self.file.close()
