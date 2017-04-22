#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
import time,datetime


def queryStockCount(stock):

	conn = MySQLdb.connect(host='localhost', port= 3306, user='jack', passwd='jack',db='jack')
	cur = conn.cursor()
	try:
		cur.execute("select count(1) from quote_data_qfq_new where stock = '" + stock + "'")
		rowcount = cur.fetchone()
	except Exception as e:
		rowcount = (0 ,1);
	else:
		pass
	finally:
		pass
	
	cur.close()
	conn.commit()
	conn.close()
	return rowcount[0]


def queryStockMaxTradeDate(stock):
	try:
		conn = MySQLdb.connect(host='localhost', port = 3306, user='jack', passwd='jack', db='jack')
		cur = conn.cursor()
		cur.execute("select max(date) from quote_data_qfq_new where stock = '" + stock + "'")
		maxDate = cur.fetchone()
		#maxDate = tmaxDate[0].strftime('%Y-%m-%d')
		print maxDate
	except Exception as e:
		maxDate = [datetime.datetime(1986, 9, 30, 0, 0, 0, 0)]
	else:
		pass
	finally:
		pass
	cur.close
	conn.commit()
	conn.close()
	return maxDate[0] + datetime.timedelta(days=1)


def downloadQuoteByStockAndDate(tRealbegin, tRealend, stock):
	now = datetime.datetime.now()
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

def log(msg):
	nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print   nowtime + ':' + msg 
