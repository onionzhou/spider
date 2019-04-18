#!/usr/bin/python3
# -*- coding:utf-8 -*-

from wxpy import  *
group_name = '一个女神和两头🐷'

def sendMessageToFriend(data):
    bot = Bot(cache_path=True)
    group = bot.groups().search(group_name)[0]
    group.send(data)
if __name__ == '__main__':
    pass