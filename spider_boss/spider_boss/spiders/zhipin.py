# -*- coding: utf-8 -*-
import scrapy
from spider_boss.items import SpiderBossItem
import logging

logger = logging.getLogger(__name__)


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/job_detail/?query=python']

    def parse(self, response):
        info_list = response.xpath('//div[@class="job-list"]//li')

        for each in info_list:
            item = SpiderBossItem()
            item["company"] = each.xpath('.//div[@class="company-text"]/h3//text()').extract_first()
            item["job_title"] = each.xpath('.//div[@class="job-title"]/text()').extract_first()
            item["money"] = each.xpath(".//span/text()").extract_first()
            item["detail_url"] = each.xpath('.//div[@class="job-title"]/../@href').extract_first()
            item["detail_url"] = "https://www.zhipin.com" + item["detail_url"]
            # logger.warning(item)

            #回调处理职位详情页
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_context_detail,
                meta={"item":item}
            )



       #next page

        next_url = response.xpath("//a[@class='next']/@href").extract_first()

        if next_url is not None:
            next_url = "https://www.zhipin.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )


    def parse_context_detail(self, response):
        item = response.meta["item"]
        item["job_context"] = response.xpath("//div[@class='job-sec']/div//text()").extract()
        # print(item)
        yield  item
