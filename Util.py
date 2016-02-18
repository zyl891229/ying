# -*- coding: utf8 -*-
import os
import shutil

class Util(object):
	def __init__(self):
		pass
	#判断服务存在与否
	def serexists(self,num_ser,root,dic):
	        pid=os.popen("ps aux|grep "+dic[num_ser]+" |grep -v grep|awk '{print $2}'").read().split()
	        if len(pid) == 0:
	                return 0
	        elif len(pid) == 1:
	                print 'PID为'+pid[0]
	                return pid
	        else:
	                print '服务启动有问题，存在多个进程，如下：'
	                print os.popen("ps aux|grep "+dic[num_ser]+" |grep -v grep").read()
	
	#杀死服务
	def killser(self,pid):
		os.popen('kill -9 '+pid[0]).read()
		print '杀死PID='+pid[0]+'的进程'
	
	#删除目录函数
	def deleteFile(self,dir):
		'''删除目录及目录下文件，再重新创建目录'''
		if os.path.exists(dir):
			if os.path.isfile(dir):
				print dir+'是文件,不是目录！-deleteFile'
			else:
				shutil.rmtree(dir)
				os.mkdir(dir)	
		else:
			print '目录不存在！-deleteFile'

	#清空日志
	def clearLog(self,num_ser,root,dic):
		os.popen('>'+root+dic[num_ser]+'/logs/catalina.out')
		print '已清空'+root+dic[num_ser]+'/logs/catalina.out'
	
	#看日志
	def viewLog(self,num_ser,root,dic):
		if self.serexists(num_ser,root,dic) == 0:
			print '服务没启动！-viewLog'
		else: 
			print '开始打印'+root+dic[num_ser]+'的日志'
			print '='*50+'我是分割线'+'='*50
			os.system('/usr/local/tool/log.sh 1 '+root+dic[num_ser])

	#看startlog
	def viewStartLog(self,num_ser,root,dic):
		if self.serexists(num_ser,root,dic) == 0:
			print '服务没启动！-viewLog'
		else: 
			print '开始打印'+root+dic[num_ser]+'的日志'
			print '='*50+'我是分割线'+'='*50
			os.system('/usr/local/tool/log.sh 3 '+root+dic[num_ser])


 	#获取服务路径
	def server_dic(self,rootdir):
		i = 0
		server_dic = {}
		for filename in os.listdir(rootdir):
			if filename.startswith(('tomcat','tomcat7')):
				i+=1
				server_dic[i]=filename
		return server_dic			
		
