#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 

def textRead(filename):
    try:
        file = open(filename)
    except IOError:
        error = []
        return error

    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]

    file.close

    return content


def printCount(datalist):

    f= open('test.txt', 'a')

    for i in range(1, 30):
        if i < 10:
            tmp = datalist.count(str(i).rjust(2,'0'))
            #print(str(i).rjust(2, '0'))
        else:
            tmp = datalist.count(str(i))
            #print(str(i))
        if not tmp == 0:
            print('num= ',i,'count= ',tmp)
            #f.write( i ,tmp)



def processData(datalist):
    tmplist = []
    tmplist2 = []
    for dataline in datalist:
        data = dataline.strip().split(' ')
        frontlist = data[:5]
        backlist = data[-2:]
        # print(data , '====',prelist ,'---', houlist)
        for i in frontlist:
            tmplist.append(i)
        for i in backlist:
            tmplist2.append(i)
            # print(tmplist , '-----',tmplist2)
    printCount(tmplist)
    print('-'*30)
    printCount(tmplist2)
    #print(tmplist.count('02'))
    #tmplist2.count('23')


if __name__ == '__main__':
    test = textRead('daletou18.txt')
    processData(test)

