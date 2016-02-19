# -*- coding: utf8 -*-
import sys
import os
import shutil
import Util
import DubboSer
import Actions
import urllib2
from bs4 import BeautifulSoup
import socket

class dubboCheck(object): 
	def check(this):
		# get the local ip
		local_ip = socket.gethostbyname(socket.gethostname())
		
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		
		top_level_url = "http://" + local_ip + ":8089/dubbo-admin/governance/services"
		username = "root"
		password = "testroot"
		# add the username and password to password manager.
		password_mgr.add_password(None, top_level_url, username, password)
		
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		
		# create "opener" (OpenerDirector instance)
		opener = urllib2.build_opener(handler)
		
		# use the opener to fetch a url
		opener.open(top_level_url)
		
		# Install the opener
		urllib2.install_opener(opener)
		
		# Now all calls to use urllib2.urlopen use our opener.
		html = urllib2.urlopen(top_level_url).read()
		
		soup = BeautifulSoup(html)

		dubbo_table = soup.find("table", attrs={"class":"list list_dubbo"})
		
		if(dubbo_table):
			dubbo_table_soup = dubbo_table
		
		# find all dubbo trs and print each dubbo's name and status.
		all_dubbo_trs = dubbo_table_soup.findAll("tr")
		
		# iterate all the trs
		print '┏'+'━'*109+'┓'
		for dubbo_tr in all_dubbo_trs:
			all_tds = dubbo_tr.findAll("td")
			if(all_tds):
				dubbo_name = all_tds[1].get_text()
				dubbo_status = all_tds[2].get_text()
				print '|= '+ dubbo_name.strip('\n')  +'-'*6+ dubbo_status.strip('\n')+\
				' '*(156-len(dubbo_name)-sys.getsizeof(dubbo_status))+'=|'
				#print 300-sys.getsizeof(dubbo_name)-sys.getsizeof(dubbo_status)
		print '┗'+'━'*109+'┛'
if __name__ == '__main__':
	dc=dubboCheck()
	dc.check()
