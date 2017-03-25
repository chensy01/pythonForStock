#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  


from sqlalchemy import create_engine
import tushare as ts
import time,datetime
import commonUtil as co


allstock = ts.get_stock_basics()

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
	

	now = datetime.datetime.now()
	#开始获取数据年份
	yearStart = int(tmpTime[0:4])
	nowyear = now.year

	tRealbegin = datetime.datetime.strptime(tmpTime, '%Y%m%d')
	tRealend = tRealbegin + datetime.timedelta(days=365)


	while (tRealbegin < now):
		strRealbegin = tRealbegin.strftime('%Y-%m-%d')
		strRealend = tRealend.strftime('%Y-%m-%d')
		if(tRealend  > now):
			strRealend = now.strftime('%Y-%m-%d')
		print 'i am getting ' + strRealbegin + ' to ' + strRealend
		tRealbegin = tRealend + datetime.timedelta(days=1)
		tRealend = tRealend + datetime.timedelta(days=365)
	
		try:
			df = ts.get_h_data(stock, start=strRealbegin, end=strRealend)
			engine = create_engine('mysql://jack:jack@127.0.0.1/jack?charset=utf8')
			#存入数据库
			#df.to_sql('tick_data',engine)
			#追加数据到现有表
			df['stock'] = stock
			df.to_sql('quote_data_qfq_new',engine,if_exists='append')
		except Exception as e:
			print "exception found" + str(e)
		else:
			pass
		finally:
			print '\n'
		
		if df is None:
			print stock + ' does not have ' + strRealbegin + ' to ' + strRealend + ' data'
			continue
		
	nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print '$$$$$$$$$$$$   ' + nowtime + ' end to get quote data of: ' + stock  +  '   $$$$$$$$$$$$' 

nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print nowtime + ' end to get quote data'		

