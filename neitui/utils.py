#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:onion
# datetime:2019/11/6 16:03
# software: PyCharm
import time
import json
import configparser
import os


def get_loacl_date():
    '''
    获取当天的日期 2019-11-06
    :return:
    '''
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def check_dir(filename):
    '''
    检查文件路径是否存在，如果不存在则创建
    :param filename:
    :return:
    '''
    path, _ = os.path.split(filename)
    if not os.path.exists(path):
        os.makedirs(path)


def write_to_json(filename, data_list):
    '''
    写入json 文件
    :param filename: xxx.json
    :param data_list: [ {'a':b},{'a1':bb} ]
    :return:
    '''
    check_dir(filename)

    with open(filename, 'w', encoding='utf-8') as fp:
        for data in data_list:
            content = json.dumps(data, ensure_ascii=False) + '\n'
            fp.write(content)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        for data in fp.readlines():
            yield json.loads(data)


def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        data = fp.readlines()
    return data


def write_file(filename, data):
    check_dir(filename)

    with open(filename, 'wb') as fp:
        fp.write(data)


def read_config(filename):
    cnf = configparser.ConfigParser()
    cnf.read(filename, encoding='utf-8')
    return cnf


