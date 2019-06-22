# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from  pymongo import MongoClient
client = MongoClient("mongodb://onion:onion@192.168.1.20:27017/boss")
collection = client["boss"]["python"]


class SpiderBossPipeline(object):
    def process_item(self, item, spider):
        collection.insert(item)
        print(item)
        return item

class SpiderBossPipeline1(object):
    def process_item(self, item, spider):
        print("301")

        return item