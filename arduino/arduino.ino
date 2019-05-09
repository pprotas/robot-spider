#include <DynamixelSerial.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define INPUT_SIZE 9

char piData[INPUT_SIZE];
int counter = 0;
int ser, pos;
int Temperature, Voltage, Position;

void setup() {
  Dynamixel.begin(1000000,2);
  delay(500);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  checkStatus();
  moveServo(ser,pos);
  Dynamixel.end();
  Serial.begin(9600);
  Serial.println(Temperature);
  Serial.println(Voltage);
  Serial.println(Position);
  Serial.end();
  Dynamixel.begin(1000000,2);
  delay(1000);
}

void receiveData(int byteCount){
  char rc = Wire.read();
  piData[counter] = rc;
  counter++;
  if(counter == INPUT_SIZE || rc == '\n') {
    counter = 0;
    separate();
    moveServo(ser, pos);
  }
}

void sendData() {
}

void separate() {
  char* separator = strchr(piData, ',');
  *separator = 0;
  ser = atoi(piData);
  ++separator;
  pos = atoi(separator); 
}

void moveServo(int servo, int position) {
  Dynamixel.move(servo, position);
}

void checkStatus() {
  Temperature = Dynamixel.readTemperature(1);
  Voltage = Dynamixel.readVoltage(1);
  Position = Dynamixel.readPosition(1);
}

