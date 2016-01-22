#!/usr/bin/env python
# -*- coding: utf-8 -*-

''
__author__ = 'kakake'

"""
ArduinoŽúÂë
byte number = 0;
void setup(){
     Serial.begin(9600);
}

void loop(){
    if (Serial.available()) {
       number = Serial.read();
       Serial.print("character recieved: ");
       Serial.println(number, DEC);
   }
}
"""


import serial
import RPi.GPIO
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.open()

#ser.write("testing")
try:
     i=0
     while 1:
              if (i==0):
              	ser.write("1")
              	i=1
              else:
	              ser.write("0")
	              i=0
              time.sleep(1)
              #response = ser.readline()
              #print response
              print 'send ok.'
              #time.sleep(1)
except KeyboardInterrupt:
     ser.close()

