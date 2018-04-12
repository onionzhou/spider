#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup
import threading
import time
baseUrl = 'http://kaijiang.500.com/shtml/dlt/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/55.0.2883.87 Safari/537.36'}
def getUrl(url):
    r = requests.get(url,headers=headers)
    if not r.status_code == 200: #状态吗为200 数字
        return None
    return r.content


def paserData(response):
    datalist =[]
    bs =  BeautifulSoup(response,'xml')
    data = bs.find(name='div',attrs={'class':'ball_box01'}).get_text()  #get 彩票结果
    data = data.replace("\n", " ").lstrip().rstrip()
    #print (data + ',')
    datalist.append(data)
    print(datalist)
    writePage(datalist)
    
def  writePage(data):
    with open('daletou18.txt','a') as f :
        for i in range(len(data)):
            f.write(str(data[i]) +' ')
        f.write('\n')


def doIt(url):
    req =getUrl(url)
    if req == None:
        return
    paserData(req)
'''
用于爬取大乐透每期的号
'''

if __name__ == '__main__':
    #url = baseUrl +'07002.shtml'
    #print (url)
    #req = getUrl(url)
    #paserData(req)
    print('doing .....')
    begin = 18001
    end = 18041
    for i in range(begin, end):
        url = baseUrl + str(i) + '.shtml'
        #print (url)
        doIt(url)
        #threading.Thread(target=doIt,args=(url)).start()
        time.sleep(1)

    print('done......-.-')

