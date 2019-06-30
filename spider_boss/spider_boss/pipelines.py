# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from  pymongo import MongoClient
from spider_boss.items import SpiderBossItem


#
# client = MongoClient("mongodb://onion:onion@192.168.1.20:27017/boss")
# client = MongoClient("mongodb://127.0.0.1:27017/boss")

# collection = client["boss"]["python"]

class DataBaseException(Exception):
    pass

class SpiderBossPipeline(object):

    def open_spider(self, spider):
        self.client = MongoClient("mongodb://127.0.0.1:27017/boss")

    def close_spider(self, spider):
        print("close ...")
        print(spider.name)
        self.client.close()

    def process_item(self, item, spider):
        # spider.settings.get("MY_USER_AGENT_LIST")
        if spider.name =="zhipin":
            self.collection = self.client["boss"]["python"]
            item["job_context"] = self.process_context(item["job_context"])
            # collection.insert(item)
            if isinstance(item, SpiderBossItem):
                self.collection.insert(dict(item))
            # print(item)
        return item

    def process_context(self, context):
        # 处理 "\n" 和空字符串
        context = [i.strip() for i in context if i.strip() != ""]
        return context

#存储测试相关的职位
class SpiderBossPipeline1(object):

    def open_spider(self, spider):
        self.client = MongoClient("mongodb://127.0.0.1:27017/boss")

    def close_spider(self, spider):

        self.client.close()

    def process_item(self, item, spider):
        if spider.name =="zhipin_test":
            self.collection = self.client["boss"]["test"]
            item["job_context"] = self.process_context(item["job_context"])
            if isinstance(item, SpiderBossItem):
                self.collection.insert(dict(item))
        return item

    def process_context(self, context):
        # 处理 "\n" 和空字符串
        context = [i.strip() for i in context if i.strip() != ""]
        return context