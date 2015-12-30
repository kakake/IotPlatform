#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'心跳处理'
__author__ = 'kakake'

from httphandle import httphandle

class heartbeathandle(httphandle):
	
	def __init__(self, name='heartbeat', interval=2,hostname=""):
		httphandle.__init__(self,name,interval,hostname)
	
	def execute(self):#重写
		data={'cmdname':'heartbeat'}
		val= self.posthttpdata('heartbeat',data)
		