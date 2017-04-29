#!/bin/bash

echo "demo is working"


while : 
do
	count=`ps -ef|grep -v 'grep'|grep saveQuoteToDb|wc -l`
	echo $count

	if [ $count -gt 0 ] 
	then
		echo 'it is alive ,i quit'
		sleep 300
        else
		python saveQuoteToDb.py >> ubuntu5.txt
	fi
done
