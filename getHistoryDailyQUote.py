#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import commonUtil as co
import tushare as ts
import time,datetime

allstock = ts.get_stock_basics()
co.log("there are " + str(len(allstock)) + " stocks total")

co.log("begin to get stock quote")
for stock in allstock.index:
	co.log('i am going to download ' + stock + ' quote data')
	co.downloadQuoteByStock(stock)
	co.log('download stock ' + stock + 'quote data complete')


co.log('program end. i have finished my job')