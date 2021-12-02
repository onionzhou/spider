#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:onion
# datetime:2019/11/12 15:55
# software: PyCharm
from neitui.Drop_jd import Neitui

def main():
    url = 'https://www.itneituiquan.com/login'
    neitui = Neitui(DEBUG=True)
    neitui.login(url)
    neitui.search_jd('测试')


if __name__ == '__main__':
    main()
