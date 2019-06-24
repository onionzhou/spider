# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from  pymongo import MongoClient
from spider_boss.items import SpiderBossItem

#
# client = MongoClient("mongodb://onion:onion@192.168.1.20:27017/boss")
client = MongoClient("mongodb://127.0.0.1:27017/boss")

collection = client["boss"]["python"]


class SpiderBossPipeline(object):
    def process_item(self, item, spider):
        item["job_context"] = self.process_context(item["job_context"])
        # collection.insert(item)
        if isinstance(item, SpiderBossItem):
            collection.insert(dict(item))
        # print(item)
        return item

    def process_context(self, context):
        #处理 "\n" 和空字符串
        context = [i.strip() for i in context if i.strip() !=""]
        return context


class SpiderBossPipeline1(object):
    def process_item(self, item, spider):
        # print("301")
        return item
