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

