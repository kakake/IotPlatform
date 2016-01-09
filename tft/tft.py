#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'GPIO处理'
__author__ = 'kakake'

import time
import RPi.GPIO
from ascii import ASCII8x16

class tft(object):
	ct=0
	#CS=17
	#RES=18
	#RS=23
	#RW=24
	CMD={'CS':17,'RES':18,'RS':23,'RW':24}
	
	#D0=20
	#D1=5
	#D2=6
	#D3=13
	#D4=19
	#D5=26
	#D6=12
	#D7=16
	DATA={'D0':20,'D1':5,'D2':6,'D3':13,'D4':19,'D5':26,'D6':12,'D7':16}
	
	X_MAX=240
	Y_MAX=320
	
	IN = RPi.GPIO.IN
	OUT = RPi.GPIO.OUT
	
	LOW = RPi.GPIO.LOW
	HIGH = RPi.GPIO.HIGH
	
	def __init__(self):
		RPi.GPIO.setmode(RPi.GPIO.BCM)
		for (i,v) in tft.CMD.items():
			RPi.GPIO.setup(v, tft.OUT)
			RPi.GPIO.output(v, False)
		for (i,v) in tft.DATA.items():
			RPi.GPIO.setup(v, tft.OUT)
			RPi.GPIO.output(v, False)
		
	def ClearScreen(self,bColor):
		self.LCD_SetPos(0,tft.X_MAX-1,0,tft.Y_MAX-1)
		for i in range(tft.Y_MAX):
			for j in range(tft.X_MAX):
				self.Write_Data_U16(bColor)
	
	def LCD_PutChar8x16(self,x,y,c,fColor,bColor):
		self.LCD_SetPos(x,x+8-1,y,y+16-1)
		m=ASCII8x16['%d' % ord(c)]
		print c,m
		#print self.writeJSON()
		for row in m:
			x=0x80
			for i in range(8):
				if(row&x>0):
					self.Write_Data_U16(bColor)
					#print 'bColor'
					#print font.writeJSON()
				else:
					self.Write_Data_U16(fColor)
					#print 'fColor'
					#print font.writeJSON()
				x=x>>1
	
	def LCD_PutChar(self,x,y,c,fColor,bColor):
		self.LCD_PutChar8x16(x,y,c,fColor,bColor)
	
	def PutGB1616(self,x,y,c,fColor,bColor):
		pass
	
	def LCD_PutString(self,x,y,s,fColor,bColor):
		l=0
		d=len(s)
		i=0
		while i<d:
			if (ord(s[i])<0x80):
				self.LCD_PutChar(x+l*8,y,s[i],fColor,bColor)
				l=l+1
			else:
				self.PutGB1616(x+l*8,y,s[i],fColor,bColor)
				l=l+2
			i=i+1
	
	def Show_RGB(self,x0,x1,y0,y1,Color):
		self.LCD_SetPos(x0,x1,y0,y1)
		for i in range(y0,y1):
			for j in range(x0,x1):
				self.Write_Data_U16(Color)
				
	def show_colour_bar(self):
		GAP=50
		self.LCD_SetPos(0,tft.X_MAX-1,0,tft.Y_MAX-1)
		for H in range(tft.X_MAX):
			for V in range(GAP*1):
				self.Write_Data_U16(0xf800)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*1,GAP*2):
				self.Write_Data_U16(0x07e0)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*2,GAP*3):
				self.Write_Data_U16(0x001f)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*3,GAP*4):
				self.Write_Data_U16(0xffe0)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*4,GAP*5):
				self.Write_Data_U16(0xf81f)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*5,GAP*6):
				self.Write_Data_U16(0x07ff)
				
		for H in range(tft.X_MAX):
			for V in range(GAP*6,GAP*7):
				self.Write_Data_U16(0xffff)
		
		for H in range(tft.X_MAX):
			for V in range(GAP*7,GAP*8):
				self.Write_Data_U16(0x0000)
				
	def Write_Data_U16(self,y):
		m=y>>8
		n=y
		self.LCD_Write_Data(m)
		self.LCD_Write_Data(n)
	
	def LCD_Write_Command(self,u):#写指令
		RPi.GPIO.output(tft.CMD['CS'],tft.LOW)
		RPi.GPIO.output(tft.CMD['RS'],tft.LOW)
		x=0x80
		for (i,v) in tft.DATA.items():
			if(u&x>0):
				RPi.GPIO.output(v, tft.HIGH)
			else:
				RPi.GPIO.output(v, tft.LOW)
			x=x>>1
		RPi.GPIO.output(tft.CMD['RW'],tft.LOW)
		RPi.GPIO.output(tft.CMD['RW'],tft.HIGH)
		RPi.GPIO.output(tft.CMD['CS'],tft.HIGH)
		#print self.writeJSON()
		
	def LCD_Write_Data(self,u):#写数据
		#tft.ct+=1	
		RPi.GPIO.output(tft.CMD['CS'],tft.LOW)
		RPi.GPIO.output(tft.CMD['RS'],tft.HIGH)
		x=0x80
		for (i,v) in tft.DATA.items():
			if(u&x>0):
				RPi.GPIO.output(v, tft.HIGH)
			else:
				RPi.GPIO.output(v, tft.LOW)
			x=x>>1
		RPi.GPIO.output(tft.CMD['RW'],tft.LOW)
		RPi.GPIO.output(tft.CMD['RW'],tft.HIGH)
		RPi.GPIO.output(tft.CMD['CS'],tft.HIGH)
		#print self.writeJSON()
		
	def WriteCom(self,a,b):
		self.LCD_Write_Command(a)
		self.LCD_Write_Command(b)
		
	def WriteData(self,a,b):
		self.LCD_Write_Data(a)
		self.LCD_Write_Data(b)
		
	def delayms(self,count):
		time.sleep(0.001*count)
		
	def TFT_Initial(self):
		RPi.GPIO.output(tft.CMD['RES'],tft.HIGH)
		self.delayms(1)
		RPi.GPIO.output(tft.CMD['RES'],tft.LOW)
		self.delayms(10)
		RPi.GPIO.output(tft.CMD['RES'],tft.HIGH)
		self.delayms(50)
		self.WriteCom(0x06,0x06)
		self.WriteData(0X00,0X00)
		self.delayms(100)
		self.WriteCom(0x00,0x07)
		self.WriteData(0X00,0X01)
		self.delayms(5)
		self.WriteCom(0x01,0x10)
		self.WriteData(0X00,0X01)
		self.delayms(5)
		self.WriteCom(0x01,0x00)
		self.WriteData(0X17,0XB0)
		self.WriteCom(0x01,0x01)
		self.WriteData(0X01,0X47)
		self.WriteCom(0x01,0x02)
		self.WriteData(0X01,0X9D)
		self.WriteCom(0x01,0x03)
		self.WriteData(0X36,0X00)
		self.WriteCom(0x02,0x81)
		self.WriteData(0X00,0X10)
		self.delayms(5)
		self.WriteCom(0x01,0x02)
		self.WriteData(0X01,0XBD)
		self.delayms(5)
		self.WriteCom(0x00,0x00)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x00,0x01)
		self.WriteData(0X01,0X00)
		self.WriteCom(0x00,0x02)
		self.WriteData(0X01,0X00)
		self.WriteCom(0x00,0x03)
		self.WriteData(0X10,0XB0)
		self.WriteCom(0x00,0x06)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x00,0x08)
		self.WriteData(0X02,0X02)

		self.WriteCom(0x00,0x09)
		self.WriteData(0X00,0X01)
		self.WriteCom(0x00,0x0B)
		self.WriteData(0X00,0X10)
		self.WriteCom(0x00,0x0C)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x00,0x0F)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x00,0x07)
		self.WriteData(0X00,0X01)

		self.WriteCom(0x00,0x10)
		self.WriteData(0X00,0X11)
		self.WriteCom(0x00,0x11)
		self.WriteData(0X03,0X01)
		self.WriteCom(0x00,0x12)
		self.WriteData(0X03,0X00)
		self.WriteCom(0x00,0x20)
		self.WriteData(0X02,0X1E)
		self.WriteCom(0x00,0x21)
		self.WriteData(0X02,0X02)

		self.WriteCom(0x00,0x90)
		self.WriteData(0X08,0X00)
		self.WriteCom(0x00,0x92)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x01,0x00)
		self.WriteData(0X12,0XB0)
		self.delayms(10)
		self.WriteCom(0x01,0x01)
		self.WriteData(0X01,0X47)
		self.delayms(10)
		self.WriteCom(0x01,0x02)
		self.WriteData(0X01,0XBE)
		self.delayms(10)
		self.WriteCom(0x01,0x03)
		self.WriteData(0X2B,0X00)
		self.delayms(10)
		self.WriteCom(0x01,0x07)
		self.WriteData(0X00,0X00)
		self.delayms(10)
		self.WriteCom(0x01,0x10)
		self.WriteData(0X00,0X01)
		self.delayms(10)
		self.WriteCom(0x02,0x10)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x11)
		self.WriteData(0X00,0XEF)
		self.WriteCom(0x02,0x12)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x13)
		self.WriteData(0X01,0X8F)
		self.WriteCom(0x02,0x00)
		self.WriteData(0X00,0X00)

		self.WriteCom(0x02,0x01)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x80)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x81)
		self.WriteData(0X00,0X07)
		self.WriteCom(0x02,0x82)
		self.WriteData(0X00,0X00)
		self.delayms(10)
		self.WriteCom(0x03,0x00)
		self.WriteData(0X01,0X01)
		self.WriteCom(0x03,0x01)
		self.WriteData(0X09,0X29)
		self.WriteCom(0x03,0x02)
		self.WriteData(0X0F,0X2C)
		self.WriteCom(0x03,0x03)
		self.WriteData(0X2C,0X0F)
		self.WriteCom(0x03,0x04)
		self.WriteData(0X29,0X09)
		self.WriteCom(0x03,0x05)
		self.WriteData(0X01,0X01)
		self.WriteCom(0x03,0x06)
		self.WriteData(0X19,0X04)
		self.WriteCom(0x03,0x07)
		self.WriteData(0X04,0X19)
		self.WriteCom(0x03,0x08)
		self.WriteData(0X06,0X05)

		self.WriteCom(0x03,0x09)
		self.WriteData(0X04,0X03)
		self.WriteCom(0x03,0x0A)
		self.WriteData(0X0E,0X06)
		self.WriteCom(0x03,0x0B)
		self.WriteData(0X0E,0X00)
		self.WriteCom(0x03,0x0C)
		self.WriteData(0X00,0X0E)
		self.WriteCom(0x03,0x0D)
		self.WriteData(0X06,0X0E)
		self.WriteCom(0x03,0x0E)
		self.WriteData(0X03,0X04)
		self.WriteCom(0x03,0x0F)
		self.WriteData(0X05,0X06)
		self.WriteCom(0x04,0x00)
		self.WriteData(0X35,0X00)
		self.WriteCom(0x04,0x01)
		self.WriteData(0X00,0X01)

		self.WriteCom(0x04,0x04)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x00)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x01)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x02)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x03)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x04)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x05,0x05)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x06,0x00)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x06,0x06)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x06,0xF0)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x07,0xF0)
		self.WriteData(0X54,0X20)
		self.WriteCom(0x07,0xF3)
		self.WriteData(0X28,0X0F)
		self.WriteCom(0x07,0xF4)
		self.WriteData(0X00,0X22)
		self.WriteCom(0x07,0xF5)
		self.WriteData(0X00,0X01)
		self.WriteCom(0x07,0xF0)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x00,0x07)
		self.WriteData(0X01,0X73)
		self.delayms(5)
		self.WriteCom(0x00,0x07)
		self.WriteData(0X00,0X61)
		self.delayms(5)
		self.WriteCom(0x00,0x07)
		self.WriteData(0X01,0X73)
		self.delayms(500)
		self.WriteCom(0x02,0x02)
		
	def LCD_SetPos(self,x0,x1,y0,y1):
		self.WriteCom(0x02,0x10)
		self.WriteData(x0>>8,x0)
		self.WriteCom(0x02,0x11)
		self.WriteData(x1>>8,x1)
		self.WriteCom(0x02,0x12)
		self.WriteData(y0>>8,y0)
		self.WriteCom(0x02,0x13)
		self.WriteData(y1>>8,y1)

		self.WriteCom(0x02,0x00)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x01)
		self.WriteData(0X00,0X00)
		self.WriteCom(0x02,0x02)
		
       
	def writeJSON(self):
		jsondata={
			"GPIO":{}
		}
		for (i,v) in tft.DATA.items():
			value = RPi.GPIO.input(v)

			jsondata['GPIO']['%d' % v]={
			    "value":value
			}
		return jsondata

if __name__ == '__main__':
	print 'started...'
	font=tft()
	print font.writeJSON()
	font.TFT_Initial()
	while True:
		print 'inited...'
		font.ClearScreen(0x0000)
		font.ClearScreen(0x00ff)
		font.ClearScreen(0xff00)
		print 'clearscreen...'
		font.show_colour_bar()	#显示彩条
		font.ClearScreen(0x00ff)
		print 'show_colour_bar...'
		font.LCD_PutString(40,40,"hellokakake520",0x0000,0xffff)
		print 'finshed...'



