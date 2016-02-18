# -*- coding: utf8 -*-
import os
import shutil
import Util

class Actions(object):
	def __init__(self):
		self.u=Util.Util()
		self.menu = {
				1:'启动(如果未启动)或重启(如果已启动)服务，并打开日志（清除旧日志）',
				2:'实时查看日志 tail -f ',
				3:'停止服务 kill -9',
				4:'清理日志 >catalina.out'
			}
		
		self.actionselect = {
				1:self.restart,
				2:self.u.viewLog,
				3:self.u.serexists,
				4:self.u.clearLog
			 }

	#操作函数
        def actions(self,num_ser,root,dic):
	        print '\n您输入的：序号 - '+str(num_ser)+'  对应服务 - '+root+dic[num_ser]
		for n in sorted(self.menu.keys()):
			print ' '*25+'┠┈ 输入'+str(n)+' '+self.menu[n]
	        print ' '*25+'┗┈ 输入q 返回上级菜单 '
		num = raw_input('\n请输入对应的需要选择操作: ')
		if num.lower() == 'q':
			welcome()
		elif int(num) in sorted(self.actionselect.keys()):
			result = self.actionselect.get(int(num))(num_ser,root,dic)
			if num == '3' and result != 0:
				self.u.killser(result)
			if num == '3' and result == 0:
				print '服务未启动！'
		else:
			print '\n输入的操作不存在，请重新输入！！！\n'
			actions(num_ser,root,dic)
	#重启服务		
	def restart(self,num_ser,root,dic):
		pid = self.u.serexists(num_ser,root,dic)
		if pid == 0:
			print '发现服务未启动，开始启动'+root+dic[num_ser]+'服务'
			#切换工作路径到bin并启动
			os.chdir(root+dic[num_ser]+'/bin')
			print os.popen('./startup.sh').read()
			self.u.viewLog(num_ser,root,dic)	
		else:
			print '停止服务'
			self.u.killser(pid)	
			print '清理旧日志'
			self.u.deleteFile(root+dic[num_ser]+'/logs')
			print '重启'+dic[num_ser]+'服务'
			os.chdir(root+dic[num_ser]+'/bin')
			print os.popen('./startup.sh').read()	
			self.u.viewLog(num_ser,root,dic)
