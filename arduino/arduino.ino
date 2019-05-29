#include <DynamixelSerial.h>
#include <Wire.h>

#define enA 9
#define in1 4
#define in2 5
#define enB 10
#define in3 6
#define in4 7

#define SLAVE_ADDRESS 0x04
#define INPUT_SIZE 14

char piData[INPUT_SIZE];
char delimiters[] = ",\n";
int servo, data;
int temperature, warmestServo;
int readCounter = -1;
int motorSpeedA = 0;
int motorSpeedB = 0;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Dynamixel.begin(1000000,2);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  checkStatus();
  moveServo(servo, data);
}

void receiveData(int byteCount){
  int counter = -1;
  while(Wire.available()){
    char rc = Wire.read();
    if(counter != -1){
      piData[counter] = rc;
    }
    counter++;
    if(counter == INPUT_SIZE || rc == '\n')
    {
      separate();
      setDirection(servo);
    }
  }
}

void sendData() {
  if(readCounter == -1) {
    Wire.write(temperature);
    readCounter++;
  }
  else if(readCounter == 0) {
    Wire.write(warmestServo);
    readCounter = -1;
  }
}

void separate() {
  char* separator = strchr(piData, ',');
  *separator = 0;
  servo = atoi(piData);
  ++separator;
  data = atoi(separator);
} 

void setDirection(int servo) {
  if (servo > 90){
    //Rechts beweegt tegengesteld van links
    switch (servo) {
    case 91:
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      break;
    case 92:
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
      break;
    case 93:
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      break;
    case 94:
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      break;
    case 95:
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      break;
     case 96:
       digitalWrite(in3, LOW);
       digitalWrite(in4, LOW);
       break;
      case 97:
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
        break;
      case 98:
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
        break;
      case 99:
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
        break;
    }
  }
}

void moveServo(int servo, int data) {
  if(servo < 90 || servo == 254){
    Dynamixel.moveSpeed(servo, data, 200);
  }
  else if(servo == 91 || servo == 93 || servo == 95) {
    analogWrite(enA, data); // Send PWM signal to motor A
  }
  else if(servo == 92 || servo == 95 || servo == 96) {   
    analogWrite(enB, data); // Send PWM signal to motor B
  }
  else {
    analogWrite(enA, data); // Send PWM signal to motor A
    analogWrite(enB, data); // Send PWM signal to motor B
  }
}

void checkStatus() {
  int readTemp, currentServo;
  for(int i = 1; i <= 5; i++) {
    currentServo = i*10;
    readTemp = Dynamixel.readTemperature(currentServo);
    if(temperature < readTemp) {
      temperature = readTemp;
      warmestServo = currentServo;
    }
  }
}






