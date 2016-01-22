// TCP_Client_Single.ino

// this example use esp8266 to connect to an Access Point and connect to SINGLE TCP Server which is at the same subnet
// such as the esp8266 is is 192.168.1.3, and the server ip is 192.168.1.1 ,then esp8266 can connect to the server

#include "esp8266.h"
#include "SoftwareSerial.h"

#define ssid		"test"		// you need to change it 
#define password	"12345678"

#define serverIP	"192.168.1.1"
#define	serverPort	"8081"

Esp8266 wifi;
SoftwareSerial mySerial(10, 11); // RX, TX	

void setup() {
	
	delay(2000);				// it will be better to delay 2s to wait esp8266 module OK
	Serial.begin(115200);
	mySerial.begin(115200);
	wifi.begin(&Serial, &mySerial);		//Serial is used to communicate with esp8266 module, mySerial is used to debug
	if (wifi.connectAP(ssid, password)) {
		wifi.debugPrintln("connect ap sucessful !");
	} else {
		while(true);
	}
	wifi.setSingleConnect();
	if (wifi.connectTCPServer(serverIP, serverPort)) {
		wifi.debugPrintln("connect to TCP server successful !");
	}
	String ip_addr;
	ip_addr = wifi.getIP();
	wifi.debugPrintln("esp8266 ip:" + ip_addr);
	
}

void loop() {

	int state = wifi.getState();
	switch (state) {
	    case WIFI_NEW_MESSAGE: 
	      wifi.debugPrintln("new message!");
	      wifi.sendMessage(wifi.getMessage());		//send the message to TCP server what it has received
	      wifi.setState(WIFI_IDLE);
	      break;
	    case WIFI_CLOSED :							//reconnet to the TCP server 
	      wifi.debugPrintln("server is closed! and trying to reconnect it!");
	      if (wifi.connectTCPServer(serverIP, serverPort)) {
	      	wifi.debugPrintln("reconnect OK!");
	      	wifi.setState(WIFI_IDLE);
	      }
	      else {
	      	wifi.debugPrintln("reconnect fail");
	      	wifi.setState(WIFI_CLOSED);
	      }
	      break;
	    case WIFI_IDLE :							
	    	int sta = wifi.checkMessage(); 
	    	wifi.setState(sta);
	    	break;
	}

}

