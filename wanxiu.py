#!/usr/bin/python2.7
# -*- coding:utf-8 -*-  
import commonUtil as co

print('please input the stock code:')
#print('')

stock = input('>')
stock = str(stock)

print 'please input the ratio of lowest price:'
ratio=str(input('>'))
#print stock
#stock='600570'

re=co.getStockDailyQuote(stock)
co.checkWanxiuQuote(stock,re,ratio)
