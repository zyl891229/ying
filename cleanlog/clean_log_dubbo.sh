#!/bin/bash
echo "开始清理日志！"
temp1=$(df|sed -n '$p'|awk {'print $3'})

for File in tomcat_AssetManagement-node tomcat_coupon-node tomcat_credit-node tomcat_fund-node tomcat_invitationcode-node tomcat_user-node tomcat_yrb-node dubbo-admin dubbo_config-web 
do
		echo "正在清理${File}/logs下的日志......"
		#./logs	
		rm -rf  /app/dubbo/${File}/logs/*.log
		rm -rf  /app/dubbo/${File}/logs/*.txt
		rm -rf  /app/dubbo/${File}/logs/*.gz
		rm -rf  /app/dubbo/${File}/logs/*.log.*
		rm -rf  /app/dubbo/${File}/temp/*
		rm -rf  /app/dubbo/${File}/temp/catalina.*.out
		echo ""  > /app/dubbo/${File}/logs/catalina.out
		if [ -d "/app/dubbo/${File}/logs/dubbo-governance.log" ];then
				echo ""  > /app/dubbo/${File}/logs/dubbo-governance.log
				echo ""  > /app/dubbo/${File}/logs/zookeeper.out
		fi
		
		#./logs/
		for ChildFile in apiinfo debug error info p2pmessage timerinfo dboperation
		do
			if [ -d "/app/dubbo/${File}/logs/${ChildFile}" ];then
				echo "正在清理${File}/logs/${ChildFile}下的日志......"
				rm -rf  /app/dubbo/${File}/logs/${ChildFile}/*.gz
				rm -rf  /app/dubbo/${File}/logs/${ChildFile}/*.tmp
				rm -rf  /app/dubbo/${File}/logs/${ChildFile}/*.log.*
				for file in /app/dubbo/${File}/logs/${ChildFile}/*.*
				do
					if [ "${file##*.}"x == "log"x ];then
				        	echo ""  > ${file}
					fi
				done
			fi
		done
done

for File1 in lender-crm-activity lender-crm-node lender-crm-read-node
do
	echo "正在清理${File1} 下的日志......"
	echo ""  > /app/dubbo/${File1}/bin/start.log
	echo ""  > /usr/local/${File1}/logs/lender-crm.log
	if [ -d "/usr/local/${File1}/logs/fetch_history.log" ];then
		echo ""  > /usr/local/${File1}/logs/fetch_history.log
	fi	
	rm -rf  /usr/local/${File1}/logs/*.log.*
done
echo "清理前可用空间为:" ${temp1}" B"
temp2=$(df|sed -n '$p'|awk {'print $3'})
echo "清理后可用空间为:" ${temp2}" B"
let temp=temp2-temp1
echo "节省空间:" ${temp}" B"
echo "清理完成！"
