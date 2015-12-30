#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'主模块'
__author__ = 'kakake'

import sys
from heartbeathandle import heartbeathandle
from gpiohandle import gpiohandle
#import test1


def main():
    #test1.test(sys.argv)
	try:
		threads={}
		
		if len(sys.argv)  == 2:
			heartbeat=new heartbeathandle('heartbeat',2,argv[1])
			threads['heartbeat']=heartbeat
			
			gpio=new gpiohandle('gpio',0.1,argv[1])
			threads['gpio']=gpio
		else:
			heartbeat=new heartbeathandle('heartbeat')
			threads['heartbeat']=heartbeat
			
			gpio=new gpiohandle('gpio')
			threads['gpio']=gpio
		
		#启动线程
		for (name, value) in threads.items():
			value.setDaemon(True)#守护线程
			value.start()
		print "Started!!!"
		
	except Exception,ex:
		print "Stopped!!!",Exception,":",ex

if __name__ == '__main__':
    main()