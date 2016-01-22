#!/usr/bin/env python
# -*- coding: utf-8 -*-

''
__author__ = 'kakake'


import serial
import RPi.GPIO
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.open()

#ser.write("testing")
try:
     i=0
     while 1:
              response = ser.readline()
              print response
              #print 'ok.'
              #time.sleep(1)
except KeyboardInterrupt:
     ser.close()

