#!/bin/bash
echo "开始清理日志！"
temp1=$(df|sed -n '$p'|awk {'print $3'})

for File in p2pweb p2padmin p2pservice credit-web paysystem supervise svsp user-web
do
		echo "正在清理${File}/logs下的日志......"
		#./logs	
		rm -rf  /app/tomcat_${File}/logs/*.log
		rm -rf  /app/tomcat_${File}/logs/*.txt
		rm -rf  /app/tomcat_${File}/logs/*.gz
		rm -rf  /app/tomcat_${File}/logs/*.log.*
		rm -rf  /app/tomcat_${File}/temp/poifiles/*
		echo ""  > /app/tomcat_${File}/logs/catalina.out
		
		#./logs/
		for ChildFile in apiinfo debug error info p2pmessage timerinfo dboperation
		do
			if [ -d "/app/tomcat_${File}/logs/${ChildFile}" ];then
				echo "正在清理${File}/logs/${ChildFile}下的日志......"
				rm -rf  /app/tomcat_${File}/logs/${ChildFile}/*.gz
				rm -rf  /app/tomcat_${File}/logs/${ChildFile}/*.tmp
				rm -rf  /app/tomcat_${File}/logs/${ChildFile}/*.log.*
				for file in /app/tomcat_${File}/logs/${ChildFile}/*.*
				do
					if [ "${file##*.}"x == "log"x ];then
				        	echo ""  > ${file}
					fi
				done
			fi
		done
done

echo "清理前可用空间为:" ${temp1}" B"
temp2=$(df|sed -n '$p'|awk {'print $3'})
echo "清理后可用空间为:" ${temp2}" B"
let temp=temp2-temp1
echo "节省空间:" ${temp}" B"
echo "清理完成！"
