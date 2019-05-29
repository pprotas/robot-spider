#include <DynamixelSerial.h>
#include <Wire.h>

#define dp  2 // Servo control pin

#define enA 9
#define in1 4
#define in2 5
#define enB 10
#define in3 6
#define in4 7

#define pp  A0 // Analog potentiometer pin

#define SLAVE_ADDRESS  0x04
#define INPUT_SIZE     14

char piData[INPUT_SIZE];
char delimiters[] = ",\n";
int servo, data; // Variables received from rPi
int temperature, warmestServo, sound; // Variables to be sent to rPi
int readCounter = -1;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Dynamixel.begin(1000000,dp);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  moveServo(servo, data);
  checkStatus();
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
    readCounter++;
  }
  else if(readCounter == 1) {
    Wire.write(sound);
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
  sound = analogRead(pp);
  Serial.println(sound);
  //sound = map(sound, <low>, <high>, 0, 100);
  currentServo = 1;
  readTemp = Dynamixel.readTemperature(1);
  if(temperature < readTemp) {
    temperature = readTemp;
    warmestServo = 1;
  }
  for(int i = 1; i < 5; i++) {
    currentServo = i*10;
    readTemp = Dynamixel.readTemperature(currentServo);
    if(temperature < readTemp) {
      temperature = readTemp;
      warmestServo = currentServo;
    }
  }
}






