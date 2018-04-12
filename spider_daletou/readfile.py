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
		content[i] = content[i][:len(content[i])-1]

	file.close

	return content

def  processData(datalist):
	tmplist = []
	tmplist2 = []
	for dataline in datalist:
		data = dataline.strip().split(' ')
		frontlist = data[:5]
		backlist = data[-2:]
		#print(data , '====',prelist ,'---', houlist)
		for i in frontlist:		
			tmplist.append(i)
		for i in backlist:
			tmplist2.append(i)
	print(tmplist , '-----',tmplist2)

	print(tmplist.count('02'))
	print(tmplist2.count('02'))



	
if __name__== '__main__':
	test= textRead('daletou1.txt')
	processData(test)
