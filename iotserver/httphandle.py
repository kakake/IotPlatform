#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'HTTP通信处理'
__author__ = 'kakake'

import threading
import time
import httplib2 
import json
from urllib import urlencode

HOST_NAME="www.efwplus.cn"
hostauthkey='00000000-0000-0000-0000-000000000000'#主机授权码GUID，由Web网站生成

#mylock = threading.RLock()#锁
#http处理线程
class httphandle(threading.Thread):
	
    baseurl_get="http://www.efwplus.cn/"#authkey,dkey   		web端接收并解析这两个参数
    baseurl_post="http://www.efwplus.cn/"#authkey,dkey,data   	web端接收并解析这三个参数
	

    def __init__(self, name, interval=0.1,hostname=""):  
        threading.Thread.__init__(self)  
        self.name = name  
        self.interval = interval  
        self.thread_stop = False
        self.hostname=hostname  
        if len(hostname)>0:
            httphandle.baseurl_get="http://"+hostname+"/Controller.aspx?controller=IotPlatform@RaspberryPiController&method=GetData&authkey="+hostauthkey
            httphandle.baseurl_post="http://"+hostname+"/Controller.aspx?controller=IotPlatform@RaspberryPiController&method=SendData&authkey="+hostauthkey
        else:
            httphandle.baseurl_get="http://"+HOST_NAME+"/Controller.aspx?controller=IotPlatform@RaspberryPiController&method=GetData&authkey="+hostauthkey
            httphandle.baseurl_post="http://"+HOST_NAME+"/Controller.aspx?controller=IotPlatform@RaspberryPiController&method=SendData&authkey="+hostauthkey
			
    def run(self): #Overwrite run() method
        while not self.thread_stop:  
            self.execute()
            time.sleep(self.interval)  
			
    def stop(self):  
        self.thread_stop = True  
		
    def gethttpdata(self,dkey=''):#获取数据
        try:
            if len(dkey)>0:
                h = httplib2.Http('.cache') #获取HTTP对象   
                resp, content = h.request(httphandle.baseurl_get+"&dkey="+dkey) #发出同步请求，并获取内容  
                #print unicode(content,'utf-8').encode('utf-8')                
                #self.log(unicode(content.decode('utf-8','ignore'),'gbk').encode('gb18030'))
                #self.log('get:'+dkey,unicode(content,'utf-8').encode('utf-8'))
                #json=unicode(content,'utf-8')
                obj=json.loads(content)#content='{"ret":0,"msg":"","data":{}}'

                if (obj['ret']==0 and len(obj['data'])>0):
                    #print obj['data']['cmdname']
                    self.log('get:'+dkey,unicode(content,'utf-8').encode('utf-8'))
                    return obj['data']
                else:
                    #self.log('get:'+dkey,unicode(content,'utf-8').encode('utf-8'))
                    return		
	        return
        except Exception,ex:
	        print "connect web get fail!!!",":",ex
			
    def posthttpdata(self,dkey='',data={}):#提交数据
		try:
			if len(dkey)>0 and len(data)>0:
				#print data
				postdata={"data":json.dumps(data)}
				h = httplib2.Http('.cache')  #获取HTTP对象 
				#resp, content = h.request(httphandle.baseurl_post+"&dkey="+dkey, "POST", urlencode(postdata),headers={'Content-Type':'applicationx-www-form-urlencoded'})
				#print httphandle.baseurl_post+"&dkey="+dkey+"&"+urlencode(postdata)
				resp, content = h.request(httphandle.baseurl_post+"&dkey="+dkey+"&"+urlencode(postdata))
				#print content
				obj=json.loads(content)#content='{"ret":0,"msg":"","data":[]}'
				if (obj['ret']==0 and len(obj['data'])>0):
					self.log('post:'+dkey,content)
					return obj['data']
				else:
					#self.log('post:'+dkey,content)
					return	
			else:
				return
		except Exception,ex:
			print "connect web post fail!!!",":",ex
			
    def execute(self):#执行，提供给子类重写
        pass
	
    def log(self,flag,text):
        #print text
        print flag,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'@'+text
