# -*- coding: utf-8 -*-
import scrapy
import logging
logger = logging.getLogger(__name__)

class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/job_detail/?query=python']

    def parse(self, response):
        info_list = response.xpath('//div[@class="job-list"]//li')

        for each  in info_list:
            item={}
            item["money"] =each.xpath(".//span/text()").extract_first()
            item["job_title"] =each.xpath('.//div[@class="job-title"]/text()').extract_first()
            item["part_url"] =each.xpath('.//div[@class="job-title"]/../@href').extract_first()
            item["company"] =each.xpath('.//div[@class="company-text"]/h3//text()').extract_first()
            # logger.warning(item)
            # print(item)
            yield  item

        #next page

        # next_url = response.xpath()
        # if next_url != :
        #     yield scrapy.Request(
        #         next_url,
        #         callback=self.parse
        #     )

