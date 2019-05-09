#include <DynamixelSerial.h>

#define INPUT_SIZE 9
#define BAUD_RATE 9600

char piData[INPUT_SIZE];
boolean newData = false;
int data1, data2;
int Temperature, Voltage, Position;

void setup() {
  Serial.begin(BAUD_RATE);
  delay(1000);
}

void loop() {
  if(Serial.available() > 0){
    receive();
  }  
  //checkStatus();
  delay(100);
}

void receive(){
  static byte ndx = 0;
  char endMarker='\n';
  char rc;
  newData = false;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    Serial.println(rc);
    if (rc != endMarker) {
      piData[ndx] = rc;
      ndx++;
      if (ndx >= INPUT_SIZE) {
        ndx = INPUT_SIZE - 1;
      }
    }
    else {
      piData[ndx] = '\0';
      ndx = 0;
      newData = true;
    }
  }

  separate();
  moveServo(data1, data2);
}

void separate() {
  char* separator = strchr(piData, ',');
  *separator = 0;
  data1 = atoi(piData);
  ++separator;
  data2 = atoi(separator);  
}

void moveServo(int servo, int position) {
  Serial.end();
  Dynamixel.begin(1000000,2);
  Dynamixel.move(servo, position);
  Dynamixel.end();
  Serial.begin(BAUD_RATE);
}

void checkStatus() {
//  Temperature = Dynamixel.readTemperature(1);
//  Voltage = Dynamixel.readVoltage(1);
//  Position = Dynamixel.readPosition(1);
}

