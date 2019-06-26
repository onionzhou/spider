#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 8:12 AM
# @Author  : onion
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy import cmdline
cmdline.execute("scrapy crawl zhipin".split())
# cmdline.execute('scrapy crawl zhipin_test'.split())
