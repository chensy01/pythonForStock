#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
import time,datetime
import pandas as pd

engine = create_engine('mysql://jack:jack@127.0.0.1/jack?charset=utf8')
dbhostip='localhost'
dbport=3306
dbuser='jack'
dbpasswd='jack'
dbname='jack'

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


def getStockDailyQuote(stock):
	result = pd.DataFrame()
	try:
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
		sqlcmd = "select * from stock_daily_quote_qfq where code = '" + stock + "'"
		result = pd.read_sql(sqlcmd, con=conn)
	except Exception as e:
		print str(e)
	else:
		pass
	finally:
		conn.close()
	return result


def getAllStock():
	result = pd.DataFrame()
	try:
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
		sqlcmd = "select distinct code from stock_daily_quote_qfq order by code"
		result = pd.read_sql(sqlcmd, con=conn)
	except Exception as e:
		print 'error found:' + str(e)
	finally:
		pass
	return result


def getRecentlyQuoteByStock(stock,day):
	result = pd.DataFrame()
	try:
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
		sqlcmd = "select * from ( " + "select * from stock_daily_quote_qfq where code = '" + stock + "' order by date desc" + ") a limit " + day
		result = pd.read_sql(sqlcmd, con=conn)
	except Exception as e:
		print 'error found:' + str(e)
	finally:
		pass
	return result


def checkWanxiuQuote(stock,re,ratio):
	re=re.sort_values(axis=0, by='date',ascending=True)  #需按照日期升序排列
	index=len(re)-1
	while index>1:
		todayClose = re.iloc[index, 3]
		todayOpen = re.iloc[index,2]
		yesterdayClose = re.iloc[index-1,3]
		yesterdayOpen = re.iloc[index-1,2]
		yesterdayHigh = re.iloc[index-1,4]
		yesterdayLow = re.iloc[index-1,5]
		#print re.iloc[index,1]
		#print 'todayClose:' + str(todayClose)
		#print 'todayOpen:' + str(todayOpen)
		#print 'yesterdayClose:' + str(yesterdayClose)
		#print 'yesterdayOpen:' + str(yesterdayOpen)
		#print 'yesterdayHigh:' + str(yesterdayHigh)
		#print 'yesterdayLow:' + str(yesterdayLow)
		#print ''
		#当天与前一天的柱体必须为一阴一阳,且柱体高度相当
		distance = abs(todayClose - todayOpen + yesterdayClose - yesterdayOpen) #柱体高度差
		try:
			total = abs(todayClose - todayOpen) #柱体高度
			percentage = distance / total
			#print re.iloc[index,1]
		except Exception as e:
			print stock + ' trade date:'  + re.iloc[index,1]  + 'has exception'
			continue
		except Warning as w:
			print stock + ' trade date:' + re.iloc[index,1]  + 'has warnning'
		finally:
			pass
		#柱体差异范围在10%之内,且柱体必须相交
		#1、第一种形态的第一条图线为阳线，第二条图线为阴线，且阴线在前阳线的实体内开盘，在前一条线的最低价之下收盘。
		#2、第二种形态的第一条图线为阴线，第二条图线为阳线，阳线在前阴线的实体内开盘，在前阴线的最高价之上收盘。
		#if(percentage <= 0.1) and  ((todayClose < todayOpen and todayOpen > yesterdayOpen and todayOpen < yesterdayClose and todayClose < yesterdayLow) or (todayClose >todayOpen and todayOpen > yesterdayClose and todayOpen < yesterdayOpen and todayClose > yesterdayHigh)):
		if((todayClose < todayOpen and todayOpen > yesterdayOpen and todayOpen < yesterdayClose and todayClose < yesterdayLow) or (todayClose >todayOpen and todayOpen > yesterdayClose and todayOpen < yesterdayOpen and todayClose > yesterdayHigh)):
			if(judgePriceIsLow(stock,todayClose,ratio)):
				print stock + ' trade date:' + str(re.iloc[index,1]) + ' is qualitified'
		index = index-1	

def judgePriceIsLow(stock,price,minestPriceRatio):
	try:
		conn = MySQLdb.connect(host=dbhostip, port = dbport, user=dbuser, passwd=dbpasswd, db=dbname)
		sqlcmd = "select min(close) as lowest from stock_daily_quote_qfq where code = '" + stock + "'"
		result = pd.read_sql(sqlcmd, con=conn)
		lowest = result.iloc[0][0]
		if((lowest * float(minestPriceRatio)) >= float(price)):
			return True
		else:
			return False
	except Exception as e:
		print 'error found:' + str(e)
	finally:
		pass
