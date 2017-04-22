#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  


from sqlalchemy import create_engine
import tushare as ts
import time,datetime
import commonUtil as co


allstock = ts.get_stock_basics()


for stock in allstock.index:
	print stock
	print allstock.ix[stock]['timeToMarket']
	tRealbegin = co.queryStockMaxTradeDate(stock)
	tRealend = tRealbegin + datetime.timedelta(days=365)

	co.log('complete stock ' + stock + ' quote begin')
	co.downloadQuoteByStockAndDate(tRealbegin,tRealend,stock)
	co.log('complete stock ' + stock + ' quote end')