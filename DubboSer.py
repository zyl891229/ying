# -*- coding: utf8 -*-
import os
import shutil
import Util
import Actions
import dubboCheck
		
class DubboSer(object):
	def __init__(self):
		pass
	#dubbo服务函数
	def dubboServer(self):
        	#调用获取服务函数        
	        rootdir=r'/app/dubbo/'          
		d = Util.Util().server_dic(rootdir)
		list = sorted(d.keys())
		dubbolist = [
				'dubbo-admin',
				'dubbo_config-web',
				'lender-crm-activity',
				'lender-crm-node',
				'lender-crm-read-node',
				'notice-sys',
				]
		i = 0
		for l in dubbolist:
			d[len(list)+i] = l
			i+=1	
		#显示列表开始   
        	print '下面是'+rootdir+'下的所有服务：'
        	print '┏┈'+'┈'*58+'┈┓'           
        	print '┃=   序号    =┃=       服务路径                             =┃'
        	for k in sorted(d.keys()):
			if os.path.exists(rootdir+d[k]):
	                	print '┃='+' '*3+str(k)+' '*(8-len(str(k)))+'=│='+' '*4+rootdir+d[k]+' '*(40-len(d[k])-len(rootdir))+'=┃'
		print '┃=   s       =┃=       服务生产消费情况                     =┃'
		print '┃=   r       =┃=       调用重启脚本                         =┃'
		print '┃=   q       =┃=       返回上级目录                         =┃'	
		print '┗┈'+'┈'*58+'┈┛'           
        	#显示列表结束
        	try:
                	num = raw_input('\n请输入对应的序号选择服务，选择q可返回上级菜单: ')
			if num.lower() == 'q':
				os.system('./ying')
			elif num.lower() == 's':
				dc=dubboCheck.dubboCheck()
				dc.check()
			elif num.lower() == 'r':
				print '开始重启zookeeper和所有dubbo服务,请稍后......'
				os.system(rootdir+'/restart_dubbo.sh')	
			elif int(num) in sorted(d.keys()):
				da=DubboActions()
				da.actions(int(num),rootdir,d)
			else:
				print '\n输入的服务不存在，请重新输入！！！\n'		
				self.dubboServer()		
        	except KeyboardInterrupt:        
                	print '\nyingTool程序终止\n'
        	except KeyError and ValueError:  
                	print '\n输入的服务不存在，请重新输入！！！\n'
                	self.dubboServer()
class DubboActions(Actions.Actions):
        #操作函数
        def actions(self,num_ser,root,dic):
		#增加dubbo特有功能
		menulist = [
				#'查看是否有提供者和消费者',
				]
		actionslist = [
				#1+1,
				]
		i = 1
		list_1 = sorted(self.menu.keys())
		list_2 = sorted(self.actionselect.keys())
		for l in menulist:
			self.menu[len(list_1)+i] = l
			self.actionselect[len(list_2)+i]=actionslist[i-1]
			i+=1
		
		print '\n您输入的：序号 - '+str(num_ser)+'  对应服务 - '+root+dic[num_ser]
                for n in sorted(self.menu.keys()):
                        print ' '*25+'┠┈ 输入'+str(n)+' '+self.menu[n]
                print ' '*25+'┗┈ 输入q 返回上级菜单 '
                num = raw_input('\n请输入对应的需要选择操作: ')
                if num.lower() == 'q':
             		ds=DubboSer()           
			ds.dubboServer()
                elif int(num) in sorted(self.actionselect.keys()):
			if dic[num_ser].startswith(('lender','notice')):
				if self.actionselect.get(int(num)) == self.restart:
					self.nohuprestart(num_ser,root,dic)
				if self.actionselect.get(int(num)) == self.u.viewLog:
				 	self.u.viewStartLog(num_ser,root,dic)	
			else:
                       		result = self.actionselect.get(int(num))(num_ser,root,dic)
			if num == '3' and result != 0:
                                self.u.killser(result)
                        if num == '3' and result == 0:
                                print '服务未启动！'
                else:
                        print '\n输入的操作不存在，请重新输入！！！\n'
                        self.actions(num_ser,root,dic)
        #tomcat重启服务               
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
	#nohup重启服务               
        def nohuprestart(self,num_ser,root,dic):
                pid = self.u.serexists(num_ser,root,dic)
                if pid == 0:
                        print '发现服务未启动，开始启动'+root+dic[num_ser]+'服务'
                        #切换工作路径到bin并启动
                        os.chdir(root+dic[num_ser]+'/bin')
			print os.popen('nohup sh start.sh >'+root+dic[num_ser]+'/bin/start.log &').read()
                        self.u.viewStartLog(num_ser,root,dic)
                else:
                        print '停止服务'
                        self.u.killser(pid)
                        print '清理旧日志'
			print os.popen('>'+root+dic[num_ser]+'/bin/start.log').read()
                        print '重启'+dic[num_ser]+'服务'
                        os.chdir(root+dic[num_ser]+'/bin')
                        print os.popen('./startup.sh').read()
                        self.u.viewStartLog(num_ser,root,dic)

		
		
