#!/usr/bin/python2.7
# -*- coding:utf-8 -*-  
import commonUtil as co
import mailUtil as mu
import time,datetime


#print stock
#stock='600570'
print 'please input the gap of day(from today):'
day=str(input('>'))
print 'please input the ratio of lowest price:'
ratio=str(input('>'))

stocks=[]
re=co.getAllStock()
for stock in re['code']:
	re=co.getRecentlyQuoteByStock(stock,day)
	result = co.checkWanxiuQuote(stock,re,ratio)
	if (result):
		stocks.append(stock)


if(len(stocks) > 0):
	path='/Users/momo/Programs/python/result/wanxiu/'
	fileName=datetime.datetime.now().strftime('%Y-%m-%d') + '.png'
	co.printKlines(stocks, path,fileName)
	if(mu.send_mail_with_attach("wanxiu","autosend",path + fileName,fileName)):
		print('mail sent success')
	else:
		print('mail sent fail')
else:
	if(mu.send_mail_without_attach("wanxiu","notfound")):
		print('mail sent success')
	else:
		print('mail sent fail')
	