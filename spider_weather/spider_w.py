#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import time
import json
import schedule
import datetime

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/55.0.2883.87 Safari/537.36'
}
#apiurl 的调用 需要在请求头Referer 添加基础url
baseurl = "http://www.weather.com.cn/weather1dn/"

urlapi = "http://d1.weather.com.cn/sk_2d/"

urlapi2 = "http://d1.weather.com.cn/dingzhi/"

areaHome = {
    'leshan':'101271401',
    'neijiang':'101271201',
    'longchang':'101271205',
    }

areaFriend = {
    'emei':'101271414',
    'jiajiang':'101271404',
}

from wxpy import  *
group_name = '一个女神和两头🐷'
#linux
#bot = Bot(console_qr=True,cache_path="wxpy.pkl")
#windows
bot = Bot(cache_path=True)
def sendMessageToFriend(data):
    #bot = Bot(cache_path=True)
    group = bot.groups().search(group_name)[0]
    group.send(data)


def get_weather(url,headers):
    try:
        r =requests.get(url=url,headers=headers)
    except:
        print("request time out ")

    r.encoding='utf-8'
    return r.text
    #return r.json
    # with open('test.html','w',encoding='utf-8') as f:
    #    f.write(r.text)

def  data_process(data):
    '返回一个json字符串'
    try :
        strs = data.split('=')[1]#.split('=')[1]
        d = json.loads(strs)
    except:
        print("data process except ")
        d = json.loads(strs.split(';')[0])

    if d is None:
        return  None

    return d

    # soup  = BeautifulSoup(data,'html.parser')
    # s =soup.find('div',class_= "minMax")
    # print(s)

def read_test():
    with open('test.html','r',encoding='utf-8') as f:
        data = f.read()
    return  data

def testapi(citycode,url):
    #t = str(time.time()).replace('.', '')[0:13]
    accessUrl = url+citycode+".html"

    redictUrl = baseurl +citycode+".shtml"

    headers['Referer'] =redictUrl

    #print(accessUrl)

    return  get_weather(url=accessUrl,headers=headers)

def get_weather_data(areaName):
    d1 =data_process(testapi(citycode=areaName, url=urlapi))
    d2 = data_process(testapi(citycode=areaName, url=urlapi2))
    message = d2['weatherinfo']['cityname'] + "\n" + \
               d2['weatherinfo']['tempn'] + " ~ "\
               + d2['weatherinfo']['temp'] + \
              "\nPM " + d1['aqi_pm25'] + \
              "\n天气 " + d2['weatherinfo']['weather'] + \
              "\n风力 " + d2['weatherinfo']['ws'] + "\n"
              #"\n注意天气变化噢"
    return message

def testCode():
    data = testapi(cityname='leshan', url=urlapi)
    d1 = data_process(data=data)
    print(d1)

    print("++++++++++++++++++++++++++")
    data = testapi(cityname='leshan', url=urlapi2)
    d = data_process(data=data)
    print(d)

    message = d['weatherinfo']['cityname'] + "\n" + \
              "最低气温 " + d['weatherinfo']['tempn'] + \
              "\n最高气温 " + d['weatherinfo']['temp'] + \
              "\nPM " + d1['aqi_pm25'] + \
              "\n天气 " + d['weatherinfo']['weather'] + \
              "\n风力 " + d['weatherinfo']['ws'] + \
              "注意天气变化噢"

    print(message)

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def test():
    localtime = get_time()
    l = []
    for key in areaFriend:
        data =get_weather_data(areaFriend[key])
        l.append(data)

    sfriend = "---\n".join(str(i) for i in l ) +"---\n" +'要注意天气变化O-O,小仙女们'
    finalsend= localtime +"\n" + sfriend
    #print(finalsend)
    sendMessageToFriend(finalsend)

    #for value in areaHome.values():
    #   print(get_weather_data(value))
def schedule_test():
    schedule.every().day.at("7:00").do(test)
    schedule.every(1).minutes.do(test)

    while True:
        schedule.run_pending()
        time.sleep(1)

    bot.join()

if __name__ == "__main__":
    #test()
    schedule_test()


