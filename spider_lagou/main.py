#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 7:18 PM
# @Author  : onion
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import re


def requests_page():
    url = "https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        ,
        "Referer": "https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput="
        , "Origin": "https://www.lagou.com"
        ,
        "Cookie": "user_trace_token=20190620215847-215df595-9369-4aa5-8afc-81a444fbfd92; _ga=GA1.2.1588186673.1561039130; LGUID=20190620215850-87dde864-9363-11e9-a42c-5254005c3644; JSESSIONID=ABAAABAAAGFABEFF56E8E579B08C04A2CE9C333D1EBC042; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1561039130,1563188870; _gid=GA1.2.1217215227.1563188870; LGSID=20190715190750-c8dda9a0-a6f0-11e9-bf31-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=5eb9ab4d8877e5de8261913651f388dfc66ba90e2d; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1563191629; LGRID=20190715195409-41a2bc6c-a6f7-11e9-a4e2-5254005c3644; SEARCH_ID=1566809367034059945b2aa124415dbf"
        , "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        , "Accept": "application/json, text/javascript, */*; q=0.01"
        , "X-Requested-With": "XMLHttpRequest"
        , "X-Anit-Forge-Token": "None"
        , "X-Anit-Forge-Code": "0"
        # ,"Accept-Encoding": "gzip, deflate, br"
        # ,"Accept-Language": "zh-CN, zh;q = 0.9"
        # ,"Connection": "keep-alive"
        # ,"Content-Length": "55"
        # ,"Host": "www.lagou.com"
    }
    data = {
        "first": "true",
        "pn": 1,
        "kd": "测试开发"
    }

    ret = requests.post(url=url, headers=headers, data=data)
    print(ret.content)


class SpiderLagou(object):
    count =0

    def __init__(self):
        self.url = "https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput="
        self.driver = webdriver.Chrome()


    def run(self):
        self.driver.get(self.url)

        while True:
            source = self.driver.page_source
            #页面解析
            #self.parse_page(source)
            try:
                next_btn =WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="pager_container"]/span[last()]'))
            )
            except:
                self.driver.quit()

            # 点击下一页
            #拉勾网在没有登陆的情况下只能连续爬取10页
            #next_btn = self.driver.find_element(By.XPATH, '//div[@class="pager_container"]/span[last()]')
            try :
                if "pager_next_disabled" not in next_btn.get_attribute("class"):
                    next_btn.click()
                    time.sleep(2)
                    self.count +=1
                    print("click it {}".format(self.count))
                else:
                    print("页面已经全部爬取完成")
                    break
            except:

                pass

    def parse_page(self, page):
        html = etree.HTML(page)
        # 获取详情页的url
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.get_detail_page(link)
            time.sleep(2)

    def get_detail_page(self, url):
        # self.driver.get(url)
        print(url)
        # 新开一个页面
        try:

            #self.driver.execute_script("window.open('"+url+"')")
            js = "window.open('{}');".format(url)
            print(js)
            self.driver.execute_script(js)
        except:
            print("你说啥")
            #self.driver.close()

        self.driver.implicitly_wait(5)
        handle = self.driver.window_handles[1]
        self.driver.switch_to.window(handle)

        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    '''
    解析详情页面
    '''

    def parse_detail_page(self, page):
        htmlElement = etree.HTML(page)
        job_title = htmlElement.xpath('//div[@class="job-name"]/@title')
        company = htmlElement.xpath('//div[@class="job-name"]/h4/text()')
        #job_requests = htmlElement.xpath('//dd[@class="job_request"]/h3//text()')
        job_requests = htmlElement.xpath('//dd[@class="job_request"]/h3//span')
        # 薪资
        money = job_requests[0].xpath("./text()")[0].strip()
        # 城市
        city = job_requests[1].xpath("./text()")[0]
        city = re.sub(r"[/\s]", "", city).strip()
        # 工作年限
        working_years = job_requests[2].xpath("./text()")[0]
        working_years = re.sub(r"[/\s]", "", working_years).strip()
        # 教育程度
        education = job_requests[3].xpath("./text()")[0]
        education = re.sub(r"[/\s]", "", education).strip()
        # 职位详情
        job_detail = htmlElement.xpath("//div[@class='job-detail']//text()")
        job_detail = "".join(job_detail).strip()
        # 公司地址
        company_url = htmlElement.xpath("//ul[@class='c_feature']//li[last()]//a[@href]//text()")[0]

        # 规模
        scale = htmlElement.xpath("//ul[@class='c_feature']//li[last()-1]/h4/text()")[0]

        info = {
            'job_title':job_title,
            'company':company,
            'money':money,
            'city':city,
            'working_years':working_years,
            'education':education,
            'job_detail':job_detail,
            'company_url':company_url,
            'scale':scale
        }
        print(info)
        #数据库操作



def main():
    lg = SpiderLagou()
    lg.run()


if __name__ == '__main__':
    main()
