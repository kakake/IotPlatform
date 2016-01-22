// TCP_Client_multi.ino

// this example use esp8266 to connect to an Access Point and connect to multiple TCP Server which is at the same subnet.
// such as the esp8266 is is 192.168.1.2, and the server ip is 192.168.1.1 ,then esp8266 can connect to the server

#include "esp8266.h"
#include "SoftwareSerial.h"

#define ssid		"test"		// you need to change it 
#define password	"12345678"

#define serverIP1	"192.168.1.1"
#define	serverPort1	"8081"

#define serverIP2	"192.168.1.1"
#define	serverPort2	"8082"

Esp8266 wifi;
SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
	
	delay(2000);				// it will be better to delay 2s to wait esp8266 module OK
	Serial.begin(115200);
	mySerial.begin(115200);
	wifi.begin(&Serial, &mySerial);  //Serial is used to communicate with esp8266 module, mySerial is used to print debug message

	if (wifi.connectAP(ssid, password)) {
		wifi.debugPrintln("connect ap sucessful !");
	} else {
		while(true);
	}

	wifi.setMultiConnect();
	if (wifi.connectTCPServer(serverIP1, serverPort1)) {
		wifi.debugPrintln("connect to TCP Server 1");
	}
	if (wifi.connectTCPServer(serverIP2, serverPort2)) {
		wifi.debugPrintln("connect to TCP Server 2");
	}

}

void loop() {

	int state = wifi.getState();
	switch (state) {
	    case WIFI_NEW_MESSAGE: 
	      wifi.debugPrintln(String(wifi.getWorkingID()) + ":" + wifi.getMessage()); //debug 
	      wifi.sendMessage(wifi.getWorkingID(), wifi.getMessage());	//sent the message back;
	      wifi.setState(WIFI_IDLE);
	      break;
	    case WIFI_CLOSED : 		// just print which connect is close, won't reconnect
	      wifi.debugPrintln(String(wifi.getFailConnectID()) + ":connect closed!"); 
	      wifi.setState(WIFI_IDLE);
	      break;
	    case WIFI_IDLE :
	    	int state = wifi.checkMessage(); 
	    	wifi.setState(state);
	    	break;
	}

}

