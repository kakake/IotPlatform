#include "esp8266.h"

Esp8266::Esp8266() {
	this->workingState = WIFI_IDLE;
	this->wifiMode = WIFI_MODE_STATION;
	this->isDebug = false;
}

void Esp8266::begin(Stream *serial){
	this->serial=serial;
}

void Esp8266::begin(Stream *serial, Stream *serialDebug){
	this->serial = serial;
	this->serialDebug = serialDebug;
	this->isDebug = true;
}

bool Esp8266::connectAP(String ssid, String password) {

	unsigned long timeout = 20000;
	unsigned long t_start = 0;
	int buf[10];
	char index=0;
 
	if (checkMode()!=WIFI_MODE_AP){
		this->wifiMode = WIFI_MODE_STATION;
	}
	else {
		if (setMode(WIFI_MODE_STATION))
			this->wifiMode = WIFI_MODE_STATION;
		else {
			if (this->isDebug) {
				debugPrintln("set mode to station false!");
			}
			return false;
		}
	}

	clearBuf();
	this->serial->println("AT+CWJAP=\""+ssid+"\",\""+password+"\"");
	t_start = millis();
	while ((millis()-t_start) < timeout) {
		while (available()>0) {
			buf[index] = read();
			if (buf[index]=='K' && buf[(index+9)%10]=='O') {
				return true;
			}
			if (buf[index]=='L' && buf[(index+9)%10]=='I' && buf[(index+8)%10]=='A' && buf[(index+7)%10]=='F') {
				return false;
			}
			index++;
			if (index==10)
				index = 0;
		}
	}
	if (this->isDebug) {
		debugPrintln("connect AP timeout");
	}
	return false;
}

int Esp8266::available() {
	return this->serial->available();
}

void Esp8266::write(String str) {
	 this->serial->println(str);
	 flush();  /*wait the data send ok, clear send_buf*/
}

bool Esp8266::checkEsp8266() {
	bool isOK=false;
	clearBuf();
	write("AT");
	delay(200);
	isOK = this->serial->findUntil("AT", "\r\n");
	if (true == isOK) {
		return true;
	} else {
		return false;
	}
}

/*clear rx_buf*/
void Esp8266::clearBuf() {
	while(available() > 0)
		read();
}

int Esp8266::read() {
	return this->serial->read();
}

String Esp8266::readData() {
	unsigned long timeout = 100;
	unsigned long t = millis();
    String data = "";
    while(millis() - t < timeout) {
    	if(available() > 0) {
	        char r = serial->read();
	        data += r;  
            t = millis();
	    }
    }
    return data;
}

bool Esp8266::setMode(char mode) {
	clearBuf();
	write("AT+CWMODE="+String(mode));
	delay(200);
	String str = readData();
	if (str.indexOf("no change") > 0)
		return true;
	else {
		if (resetEsp8266()) {
			this->wifiMode = mode;
			return true;
		}
		else {
			return false;
		}
	}

}

/*clear send_buf*/
void Esp8266::flush() {
	this->serial->flush();
}

char Esp8266::checkMode() {
	clearBuf();
	write("AT+CWMODE?");
	delay(200);
	String str = readData();
	// Serial.println(str);
	if (str.indexOf('1') > 0 )  
		return '1';
	else if (str.indexOf('2') > 0)
		return '2';
	else if (str.indexOf('3') > 0)
		return '3';
	else 
		return '0';
}

bool Esp8266::resetEsp8266() {

	unsigned long timeout = 7000;
	unsigned long t_start = 0;
	int buf[10];
	char index=0;

	clearBuf();
	write("AT+RST");
	t_start = millis();
	while ((millis()-t_start) < timeout) {
		while (available()>0) {
			buf[index] = read();
			if (buf[index]=='y' && buf[(index+9)%10]=='d' && buf[(index+8)%10]=='a' && buf[(index+7)%10]=='e' && buf[(index+6)%10]=='r') {
				return true;
			}
			index++;
			if (index==10)
				index = 0;
		}
	}
   	if (this->isDebug) {
		debugPrintln("rest esp8266 timeout");
	}
	return false;	
}


void Esp8266::debugPrintln(String str) {
	this->serialDebug->println(str);
}


bool Esp8266::setMux(int flag) {
	String str;
	clearBuf();
	write("AT+CIPMUX="+String(flag));
	delay(100);
	str = readData();
	if (str.indexOf("OK")>0 || str.indexOf("link is builded")>0)
		return true;
	else 
		return false;
}

bool Esp8266::setSingleConnect() {
	this->connectID = 0;
	this->multiFlag = false;
	return setMux(0);
}

bool Esp8266::setMultiConnect() {
	this->connectID = 0;
	this->multiFlag = true;
	return setMux(1);
}

bool Esp8266::connectTCPServer(String serverIP, String serverPort) {
	unsigned long timeout = 5000;
	unsigned long t_start = 0;
	unsigned char buf[10];
	unsigned char index=0;

	clearBuf();
	if (!this->multiFlag) {
		write("AT+CIPSTART=\"TCP\",\"" + serverIP + "\"," + serverPort);	
		t_start = millis();
		while((millis())-t_start < timeout)	{
			while(available()) {
				buf[index] = read();
				if (buf[index]=='T' && buf[(index+9)%10]=='C' && buf[(index+8)%10]=='E' && buf[(index+7)%10]=='N'
									&& buf[(index+6)%10]=='N' && buf[(index+5)%10]=='O' && buf[(index+4)%10]=='C') {
					return true;
				}
				index++;
				if (index==10)
					index = 0;			
			}
		}
		if (this->isDebug) {	
			debugPrintln("connectTCPServer timeout");
		}
		return false;
	} else {
		write("AT+CIPSTART="+ String(this->connectID) + ",\"TCP\",\"" + serverIP + "\"," + serverPort);
		t_start = millis();
		while((millis())-t_start < timeout)	{
			while(available()) {
				buf[index] = read();
				if (buf[index]=='T' && buf[(index+9)%10]=='C' && buf[(index+8)%10]=='E' && buf[(index+7)%10]=='N'
									&& buf[(index+6)%10]=='N' && buf[(index+5)%10]=='O' && buf[(index+4)%10]=='C') {
					this->connectID++;
					return true;
				}
				index++;
				if (index==10)
					index = 0;			
			}
		}
		if (this->isDebug) {
			debugPrintln("connectTCPServer timeout");
		}
		return false;		
	}
}


int Esp8266::getState() {
	return this->workingState;
}

void Esp8266::setState(int state) {
	this->workingState = state;
}
int Esp8266::checkMessage() {
	String tmp="";
	tmp = readData();
	if (tmp!="") {
		if (tmp.substring(2, 6) == "+IPD") {
			if (!(this->multiFlag)) {
				int index = tmp.indexOf(":");
				int length = tmp.substring(7, index+1).toInt();
				this->message = tmp.substring(index+1, index+length+1);
				return WIFI_NEW_MESSAGE;
			} else {
				int id = 0, length=0, index=0; 
				id = tmp.substring(7, 8).toInt();
				index = tmp.indexOf(":");
				length = tmp.substring(9, index+1).toInt();
				this->workingID = id;
				this->message = tmp.substring(index+1, index+length+1);
				return WIFI_NEW_MESSAGE;
			}
		} else if (tmp.substring(0,6) == "CLOSED" || (tmp.charAt(1)==',' && tmp.substring(2,8)=="CLOSED")) {
			if (!(this->multiFlag)) {
				return WIFI_CLOSED;
			} else {
				this->failConnectID = tmp.charAt(0)-'0';
				return WIFI_CLOSED;
			}
		} else if (tmp.substring(1,9) == ",CONNECT") {
			int index = tmp.charAt(0)-'0';
			this->workingID = index;
			return WIFI_CLIENT_ON;
		} else if (this->isPureDataMode) {
			this->message = tmp;
			return WIFI_NEW_MESSAGE;
		} else {
			return WIFI_IDLE;
		}
	} else {
		return this->workingState;
	}
}

String Esp8266::getMessage() {
	return this->message;
}

bool Esp8266::sendMessage(String str) {
	if (this->isPureDataMode) {
		this->serial->print(str);
	} else {
		String tmp = "";
		int index = 0;
		int len = 0;
		len = str.length();
		write("AT+CIPSEND="+String(len));
		delay(20);
		this->serial->print(str);

		tmp = readData();
		index = tmp.length();
		if (tmp.substring(index-9, index-2) == "SEND OK") {
			return true;
		} else {
			return false;
		}
	}
}

bool Esp8266::sendMessage(int index, String str) {
	
	String tmp = "";
	int i = 0;
	int len = 0;

	len = str.length();
	write("AT+CIPSEND="+String(index)+","+String(len));
	delay(20);
	this->serial->print(str);

	tmp = readData();
	i = tmp.length();
	if (tmp.substring(i-9, i-2) == "SEND OK") {
		return true;
	} else {
		return false;
	}
}

int Esp8266::getWorkingID() {
	return this->workingID;
}

int Esp8266::getFailConnectID() {
	return this->failConnectID;
}

bool Esp8266::openTCPServer(int port, int timeout) {
	if (setMux(1)) {
		String str="";
		write("AT+CIPSERVER=1,"+String(port));
		str = readData();
		if (str.indexOf("OK")) {
			write("AT+CIPSTO="+String(timeout));
			str = readData();
			if (str.indexOf("OK")) {
				return true;
			} else {
				return false;
			}
		} else {
			return false;
		}
	} else {
		return false;
	}	
}

bool Esp8266::enableAP(String ssid, String password) {
	if (setMode(WIFI_MODE_AP)) {
		write("AT+CWSAP=\""+ssid+"\",\""+password+"\","+String(10)+String(4));
		String tmp;
		tmp = readData();
		if (tmp.indexOf("OK")>0) {
			return true;
		} else {
			return false;
		}
	}
}

String Esp8266::getIP() {
	write("AT+CIFSR");
	String tmp = readData();
	if (this->wifiMode == WIFI_MODE_STATION) {
		int index1 = tmp.indexOf("STAIP");
		int index2 = tmp.indexOf("+CIFSR:STAMAC");
		this->staIP =  tmp.substring(index1+7, index2-3);
		return this->staIP;
	} else {
		int index1 = tmp.indexOf("APIP");
		int index2 = tmp.indexOf("+CIFSR:APMAC");		
		this->apIP =  tmp.substring(index1+6, index2-3);	
		return this->apIP;
	}	
}

bool Esp8266::setPureDataMode() {
	write("AT+CIPMODE=1");
	String tmp = readData();
	if (tmp.indexOf("OK")>0) {
		write("AT+CIPSEND");
		this->isPureDataMode = true;
		return true;
	} else
		return false;
}