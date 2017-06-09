#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
import time,datetime

engine = create_engine('mysql://jack:jack@127.0.0.1/jack?charset=utf8')
<<<<<<< HEAD
=======
dbhostip='localhost'
dbport=3306
dbuser='jack'
dbpasswd='jack'
dbname='jack'
>>>>>>> 4b51e49681604773c1ce1760416c8742e2467cd3
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
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
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
	if maxDate is None:
		maxDate = [datetime.datetime(1986, 9, 30, 0, 0, 0, 0)]  
	cur.close
	conn.commit()
	conn.close()
	if(maxDate[0] is None):
		maxDate[0] = datetime.datetime(1986, 9, 30, 0, 0, 0, 0)
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
			
			#存入数据库
			#df.to_sql('tick_data',engine)
			#追加数据到现有表
			df['stock'] = stock
			df.to_sql('quote_data_qfq_new',engine,if_exists='append')
		except Exception as e:
			print "exception found" + str(e)
			df = None
		else:
			pass
		finally:
			print '\n'
		
			if df is None:
				print stock + ' does not have ' + strRealbegin + ' to ' + strRealend + ' data'
			#	continue

def downloadQuoteByStock(stock):
	now = datetime.datetime.now()
	strBegin = queryStockMaxTradeDateInDaily(stock).strftime('%Y-%m-%d')
	strEnd = now.strftime('%Y-%m-%d')
	try:
		df = ts.get_k_data(code=stock, ktype='D', autype='qfq', start=strBegin, end=strEnd)
		df.to_sql('stock_daily_quote_qfq',engine,if_exists='append')
	except Exception as e:
		print "exception found " + str(e)
		df = None
	else:
		pass
	finally:
		print '\n'
	if df is None:
		print 'stock ' + stock + ' does not have quote data'
	else:
		print 'stock ' + stock + ' download completed'

def log(msg):
	nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print   nowtime + ':' + msg 


def queryStockMaxTradeDateInDaily(stock):
	try:
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
		cur = conn.cursor()
		cur.execute("select max(date) from stock_daily_quote_qfq where code = '" + stock + "'")
		maxDate = cur.fetchone()
		#maxDate = tmaxDate[0].strftime('%Y-%m-%d')
		print maxDate
	except Exception as e:
		print str(e)
		maxDate = [datetime.datetime(1986, 9, 30, 0, 0, 0, 0)]
	else:
		pass
	finally:
		pass
	if maxDate is None:
		maxDate = [datetime.datetime(1986, 9, 30, 0, 0, 0, 0)]  
	cur.close
	conn.commit()
	conn.close()
	if(maxDate[0] is None):
		return  datetime.datetime(1986, 9, 30, 0, 0, 0, 0)
	return maxDate[0] + datetime.timedelta(days=1)
