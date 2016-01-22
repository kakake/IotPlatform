#ifndef _ESP8266_H_
#define _ESP8266_H_

#include <Arduino.h>
#include <Stream.h>
#include <avr/pgmspace.h>
#include <IPAddress.h>

#define	WIFI_IDLE			1
#define WIFI_NEW_MESSAGE	2
#define WIFI_CLOSED			3
#define WIFI_CLIENT_ON		4

#define WIFI_MODE_STATION			'1'
#define WIFI_MODE_AP				'2'
#define WIFI_MODE_BOTH				'3'

class Esp8266
{
public:
	Esp8266();
	void begin(Stream *serial);
	void begin(Stream *serial,Stream *serialDebug);
	void comSend();
	bool connectAP(String ssid, String password);
	bool checkEsp8266();
	bool resetEsp8266();
	void debugPrintln(String str);
	bool setSingleConnect();
	bool setMultiConnect();
	bool connectTCPServer(String serverIP, String serverPort);	
	int	 checkMessage();
	String getMessage();
	void setState(int state);
	int getState();	
	bool sendMessage(String str);
	bool sendMessage(int index, String str);
	int getWorkingID(); 
	int getFailConnectID();
	bool openTCPServer(int port, int timeout);
	bool enableAP(String ssid, String password);
	String getIP();
	bool setPureDataMode();

private:
	int available();
	void write(String str);
	void clearBuf();
	int read();
	String readData();
	void flush();	
	bool setMode(char mode);
	char checkMode();	
	bool setMux(int flag);


private:
	Stream *serial;                                            
	Stream *serialDebug;
	int connectID;
	int workingID;
	int failConnectID;
	bool multiFlag;
	int workingState;
	String message;
	char wifiMode;
	String staIP;
	String apIP;
	bool isDebug;
	bool isPureDataMode;
};

#endif 