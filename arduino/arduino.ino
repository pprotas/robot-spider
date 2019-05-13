#include <DynamixelSerial.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define INPUT_SIZE 9

char piData[INPUT_SIZE];
int counter = -1;
int ser, pos;
int Temperature, Voltage, Position;
int readCounter = 0;

void setup() {
  Dynamixel.begin(1000000,2);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  //checkStatus();
  //moveServo(ser,pos);
  delay(1000);
}

void receiveData(int byteCount){
  while(Wire.available()){
    char rc = Wire.read();
    if(counter != -1){
      piData[counter] = rc;
    }
    counter++;
    if(counter == INPUT_SIZE || rc == '\n')
    {
      counter = -1;
      separate();
    }
  }
}

void sendData() {
//  if(readCounter == 0) {
//    Wire.write(Temperature);
//    readCounter++;
//  }
//  else if(readCounter == 1) {
//    Wire.write(Voltage);
//    readCounter++;
//  }
//  else if(readCounter == 2) {
//    Position = map(Position, 0, 1023, 0, 255);
//    Wire.write(Position);
//    readCounter = 0;
//  }
  Dynamixel.end();
  Serial.begin(9600);
  Serial.println("Request");
  Serial.end();
  Dynamixel.begin(1000000,2);
}

void separate() {
  char* separator = strchr(piData, ',');
  *separator = 0;
  ser = atoi(piData);
  ++separator;
  pos = atoi(separator); 
  Serial.println(ser);
  Serial.println(pos);
}

void moveServo(int servo, int position) {
   Dynamixel.move(servo, position);
}

void checkStatus() {
  Temperature = Dynamixel.readTemperature(1);
  Voltage = Dynamixel.readVoltage(1);
  Position = Dynamixel.readPosition(1);
}


