#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  


import commonUtil as co


hasQuote = co.queryStockCount('000005')
if(hasQuote >= 1):
		print 'already has'