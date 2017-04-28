#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import commonUtil as co
import tushare as ts
import time,datetime

allstock = ts.get_stock_basics()
print "there are " + len(allstock) + " stocks total"

allstock
print 'test'
nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print nowtime + ' begin to get quote data'

for stock in allstock.index:

	hasQuote = co.queryStockCount(stock)
	if(hasQuote >= 1):
		print  stock  + ' already has quote in database.quit '
		continue
	nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print '$$$$$$$$$$$$' + nowtime + ' begin to get quote data of: ' + stock  + '$$$$$$$$$$$$$$'
	#print stock
	#print allstock.ix[stock]['timeToMarket']
	tmpTime = str(allstock.ix[stock]['timeToMarket']) #上市时间点
	if len(tmpTime) != 8:   #如果获取不到就算了
		continue
	


	tRealbegin = datetime.datetime.strptime(tmpTime, '%Y%m%d')
	tRealend = tRealbegin + datetime.timedelta(days=365)


	co.downloadQuoteByStockAndDate(tRealbegin,tRealend,stock)
		
	nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print '$$$$$$$$$$$$   ' + nowtime + ' end to get quote data of: ' + stock  +  '   $$$$$$$$$$$$' 

nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print nowtime + ' end to get quote data'		

