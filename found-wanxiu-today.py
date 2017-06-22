#!/usr/bin/python2.7
# -*- coding:utf-8 -*-  
import commonUtil as co


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



path='/Users/momo/Programs/python/result/wanxiu/'
co.printKlines(stocks, path)
	