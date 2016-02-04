#!/bin/bash
if [ $1 -eq 1 ];then
	tail -f $2/logs/catalina.out
elif [ $1 -eq 2 ];then
	tail -fn100 $2/logs/catalina.out
fi
