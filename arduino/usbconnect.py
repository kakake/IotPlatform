#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Æô¶¯'
__author__ = 'kakake'

"""
Arduino´úÂë
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
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.open()

ser.write("testing")
try:
     while 1:
              response = ser.readline()
              print response
except KeyboardInterrupt:
     ser.close()
