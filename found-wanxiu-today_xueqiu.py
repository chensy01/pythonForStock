#!/usr/bin/python2.7
# -*- coding:utf-8 -*-  
import commonUtil as co


#print stock
#stock='600570'
print 'please input the gap of day(from today):'
day=str(input('>'))
print 'please input the ratio of lowest price:'
ratio=str(input('>'))

re=co.getAllStock()
for stock in re['code']:
	re=co.getRecentlyQuoteByStock(stock,day)
	co.checkWanxiuQuoteXueQiu(stock,re,ratio)

