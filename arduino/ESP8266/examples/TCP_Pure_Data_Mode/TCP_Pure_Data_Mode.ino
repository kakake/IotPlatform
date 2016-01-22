// TCP_Pure_Data_Mode.ino

// in this example ,esp8266 conneted to a TCP Server ,and working in pure data mode

#include "esp8266.h"
#include "SoftwareSerial.h"

#define	ssid		"test"
#define	password	"12345678"
#define	serverIP	"192.168.1.1"
#define serverPort	"8081"

Esp8266 wifi;
SoftwareSerial mySerial(10, 11); // RX, TX	

void setup() {

	delay(2000);				// it will be better to delay 2s to wait esp8266 module OK
	Serial.begin(115200);
	mySerial.begin(115200);
	wifi.begin(&Serial, &mySerial);		//Serial is used to communicate with esp8266 module, mySerial is used to debug

	if (wifi.checkEsp8266()) {
		wifi.debugPrintln("esp8266 is online!");
	}
	if (wifi.connectAP(ssid, password)) {
		wifi.debugPrintln("esp8266 is connected to AP!");
	}
	if (wifi.setSingleConnect()) {
		wifi.debugPrintln("single connect!");
	}
	wifi.debugPrintln(wifi.getIP());
	if (wifi.connectTCPServer(serverIP, serverPort)) {
		wifi.debugPrintln("connect TCP server OK!");
	}	
	wifi.setPureDataMode();	

}

void loop() {
	String str="";

	int state = wifi.getState();
	switch (state) {
	    case WIFI_NEW_MESSAGE: 
	      wifi.debugPrintln(wifi.getMessage());
	      str = wifi.getMessage();
	      if (str != "+++") {
	      	wifi.sendMessage(wifi.getMessage());		//send the message to TCP server what it has received
	      }
	      wifi.setState(WIFI_IDLE);
	      break;
	    case WIFI_IDLE :							
	    	int sta = wifi.checkMessage(); 
	    	wifi.setState(sta);
	    	break;
	}

}

