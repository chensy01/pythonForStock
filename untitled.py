#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  


from sqlalchemy import create_engine
import tushare as ts
import time,datetime


allstock = ts.get_stock_basics()


for stock in allstock.index:
	print stock
	print allstock.ix[stock]['timeToMarket']
	tmpTime = str(allstock.ix[stock]['timeToMarket']) #上市时间点
	if len(tmpTime) != 8:   #如果获取不到就算了
		continue
	

	now = datetime.datetime.now()

	
	strRealbegin = now.strftime('%Y-%m-%d')
	strRealend = now.strftime('%Y-%m-%d')
	print 'i am getting ' + stock + ' from ' + strRealbegin + ' to ' + strRealend
	
	try:
		df = ts.get_h_data(stock, start=strRealbegin, end=strRealend)
		engine = create_engine('mysql://jack:jack@127.0.0.1/jack?charset=utf8')
		df['stcok'] = stock
		df.to_sql('quote_data_qfq',engine,if_exists='append')
	except Exception as e:
		pass
	else:
		pass
	finally:
		pass	
	