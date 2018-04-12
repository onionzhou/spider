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

	for dataline in datalist:
		data = dataline.strip().split(' ')
		print(data)
		#tmplist.append(data)
	
if __name__== '__main__':
	test= textRead('daletou1.txt')
	
	processData(test)
