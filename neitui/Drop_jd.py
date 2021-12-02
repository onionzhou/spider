#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:onion
# datetime:2019/11/12 11:26
# software: PyCharm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from lxml import etree
import time
from neitui.utils import *
import requests

CONFIG_FILE='./config/my_conf.ini'
cnf = read_config(CONFIG_FILE)

class Neitui:

    def __init__(self,DEBUG=False):
        if DEBUG:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS()

    def login(self, url):
        # url=''https://www.itneituiquan.com/login
        self.driver.maximize_window()
        self.driver.get(url)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.login-submit-btn'))
            )
        except:
            print('not found')
            self.driver.quit()

        self.driver.find_element(By.ID, 'tab-password').click()

        self.get_verif_picture()
        self.show_image()
        input_list = self.driver.find_elements(By.CSS_SELECTOR, '.el-input__inner')
        account = input_list[0]
        passwd = input_list[1]
        verif_code = input_list[2]

        # cnf = read_config(CONFIG_FILE)
        code = input('请输入验证码： ')
        account.send_keys(cnf['account']['user'])
        passwd.send_keys(cnf['account']['passwd'])
        verif_code.send_keys(code)

        self.driver.find_element(By.CSS_SELECTOR, '.login-submit-btn').click()

    def get_verif_picture(self):
        pic_url = self.driver.find_element(By.CLASS_NAME, 'captcha-wraper'). \
            find_element_by_tag_name('img').get_attribute('src')
        res = requests.get(pic_url)

        image_path = cnf['path']['image_path']
        image_data = res.content
        write_file(image_path,image_data)

    def search_jd(self, job_name):

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.searchVal'))
            )
        except:
            print('not found')
            self.driver.quit()

        self.driver.find_element(By.CSS_SELECTOR, '.searchVal') \
            .find_element(By.CSS_SELECTOR, '.el-input__inner') \
            .send_keys(job_name)

        self.driver.find_element(By.CLASS_NAME, 'searchBtn').click()
        time.sleep(5)
        # driver.implicitly_wait(10)
        source = self.driver.page_source

        # 处理jd
        job_lists = self.get_jobs(source)

        date_str = get_loacl_date()

        # write_to_json(date_str + '.json', job_lists)
        # for job_list in read_json(date_str + '.json'):
        for job_list in job_lists:
            part_url = job_list['jd_detail_url']
            url = 'https://www.itneituiquan.com' + part_url
            detail = self.get_jobs_requirements(url)
            job_list['jd_detail'] = detail
            self.is_drop(detail)

        write_to_json('./data/'+date_str + '.json', job_lists)

    @staticmethod
    def show_image():
        image = Image.open(cnf['path']['image_path'])
        image.show()

    def is_drop(self, data_str):
        '''
        是否投递简历
        :param data_str:
        :return:
        '''
        is_throw = self.match_jd(data_str)
        # print('*' * 20)
        # print(is_throw)
        if is_throw:
            self.throw_resume()
            # 写入投递日志
        else:
            pass
            # print('技术栈不匹配')
            # 写入日志

    def throw_resume(self):
        '''投递简历'''
        all_elment = self.driver.find_element(By.CLASS_NAME, 'content-right')
        # 最后一份简历为自己最新的简历
        all_elment.find_elements(By.CLASS_NAME, 'resume')[-1].click()
        # 投递
        all_elment.find_element(By.CLASS_NAME, 'el-button').click()

    def get_jobs_requirements(self, url):
        '''获取招聘岗位的工作职责和要求'''

        self.driver.get(url)
        time.sleep(5)
        source = self.driver.page_source

        htmlelement = etree.HTML(source)
        results_list = htmlelement.xpath("//div[@class='job-detail-main-left']//text()")
        data_str = ' '.join(results_list)
        data_str = data_str.lower()

        return data_str

    def match_jd(self, data_str):
        '''
        :param data_list:获取的jd 详情
        :return: True 可以投递 Flase 忽略该JD
        '''
        count = 0
        Threshold=cnf['other']['suitability']
        my_jd_list = read_txt(cnf['path']['jd_path'])
        for key in my_jd_list:
            if data_str.find(key.strip()) != -1:
                count = count + 1
        # print(count)
        if count >= Threshold:
            return True
        else:
            return False

    def get_jobs(self, page):
        '''
        获取公司的基本信息
        :param page:
        :return:
        '''
        job_lists = []
        htmlelement = etree.HTML(page)
        # parser = etree.HTMLParser(encoding="utf-8")
        # htmlelement = etree.parse("C:\\Users\\onion\\Downloads/1.html", parser=parser)
        # print(etree.tostring(htmlelement, encoding="utf-8").decode("utf-8"))
        jd_lists = htmlelement.xpath("//div[@class='contentLeft']//div[@class='recruit']")
        for jd_list in jd_lists:
            jd_dict = {}
            try:
                # 详情页url
                jd_detail_url = jd_list.xpath("./div[@class='recruitLeft']//@href")
                # 职位
                jd_title = jd_list.xpath("./div[@class='recruitLeft']//p[@class='title']/text()")
                jd_salary = jd_list.xpath("./div[@class='recruitLeft']//p[@class='recruitSalary']/text()")
                # 位置
                jd_localtion = jd_list.xpath("./div[@class='recruitLeft']/div[@class='detail']//span[1]//text()")
                # 年限
                jd_years = jd_list.xpath("./div[@class='recruitLeft']/div[@class='detail']//span[3]/text()")
                # 学历
                jd_education = jd_list.xpath("./div[@class='recruitLeft']/div[@class='detail']//span[5]/text()")
                # 发布时间
                jd_release_time = jd_list.xpath("./div[@class='recruitLeft']/p[@class='time']/text()")
                if jd_release_time != []:
                    jd_release_time = jd_release_time[0]  # 字符串
                    jd_release_time = jd_release_time[3:]  # 切片
                # 公司名
                jd_company = jd_list.xpath("./div[@class='recruitRight']/div[@class='company']//a/text()")
                # 公司主页
                jd_company_home = jd_list.xpath("./div[@class='recruitRight']/div[@class='company']//@href")
                # 公司的标签
                jd_company_detail = jd_list. \
                    xpath("./div[@class='recruitRight']/div[@class='company']//div[@class='detail']//text()")
                if jd_company_detail != []:
                    jd_company_label = jd_company_detail[0]
                    jd_company_scale = jd_company_detail[1]
                else:
                    jd_company_label = []
                    jd_company_scale = []
            except:
                pass

            jd_dict['jd_title'] = jd_title[0]
            jd_dict['jd_detail_url'] = jd_detail_url[0]
            jd_dict['jd_salary'] = jd_salary[0]
            jd_dict['jd_localtion'] = jd_localtion[0]
            jd_dict['jd_years'] = jd_years[0]
            jd_dict['jd_education'] = jd_education[0]
            jd_dict['jd_release_time'] = jd_release_time
            jd_dict['jd_company'] = jd_company[0]
            jd_dict['jd_company_home'] = jd_company_home[0]
            jd_dict['jd_company_label'] = jd_company_label
            jd_dict['jd_company_scale'] = jd_company_scale

            # 数据库插入
            job_lists.append(jd_dict)

        return job_lists
