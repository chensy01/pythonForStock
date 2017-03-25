#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  

import MySQLdb


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
	conn = MySQLdb.connect(host='localhost', port = 3306, user='jack', passwd='jack', db='jack')
	cur = conn.cursor()
	try:
		cur.execute("select max(date) from quote_data_qfq_new where stock = '" + stock + "'")
		tmaxDate = cur.fetchone()
		maxDate = tmaxDate[0].strftime('%Y-%m-%d')
		print maxDate
	except Exception as e:
		maxDate = ('1986-09-30');
	else:
		pass
	finally:
		pass
	cur.close
	conn.commit()
	conn.close()
	return maxDate


