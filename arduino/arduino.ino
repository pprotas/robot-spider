#include <DynamixelSerial.h>
#include <Wire.h>

#define dp 2 // Servo control pin

#define enA 9
#define in1 4
#define in2 5
#define enB 10
#define in3 6
#define in4 7

#define vu0 A0 // VU
#define vu1 A1
#define vu2 A2

#define pow0  A3

#define SLAVE_ADDRESS  0x04
#define INPUT_SIZE     14


char piData[INPUT_SIZE];
char delimiters[] = ",\n";
int servo, data; // Variables received from rPi
int temperature, warmestServo, sound0, sound1, sound2, power; // Variables to be sent to rPi
int readCounter = -1;

void setup()
{
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Dynamixel.begin(1000000, dp);
  //Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop()
{
  moveServo(servo, data);
  checkStatus();
}

void receiveData(int byteCount)
{
  int counter = -1;
  while (Wire.available())
  {
    char rc = Wire.read();
    if (counter != -1)
    {
      piData[counter] = rc;
    }
    counter++;
    if (counter == INPUT_SIZE || rc == '\n')
    {
      separate();
      setDirection(servo);
    }
  }
}

void sendData()
{
  if (readCounter == -1)
  {
    Wire.write(temperature);
    readCounter++;
  }
  else if (readCounter == 0)
  {
    Wire.write(warmestServo);
    readCounter++;
  }
  else if (readCounter == 1)
  {
    Wire.write(sound0);
    readCounter++;
  }
  else if (readCounter == 2)
  {
    Wire.write(sound1);
    readCounter++;
  }
  else if (readCounter == 3)
  {
    Wire.write(sound2);
    readCounter++;
  }
  else if(readCounter == 4) {
    Wire.write(power);
    readCounter = -1;
  }
}

void separate()
{
  char *separator = strchr(piData, ',');
  *separator = 0;
  servo = atoi(piData);
  ++separator;
  data = atoi(separator);
}

void setDirection(int servo)
{
  if (servo > 90)
  {
    //Rechts beweegt tegengesteld van links
    switch (servo)
    {
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
    Dynamixel.moveSpeed(servo, data, 50);
  }
  else if (servo == 91 || servo == 93 || servo == 95)
  {
    analogWrite(enA, data); // Send PWM signal to motor A
  }
  else if (servo == 92 || servo == 95 || servo == 96)
  {
    analogWrite(enB, data); // Send PWM signal to motor B
  }
  else
  {
    analogWrite(enA, data); // Send PWM signal to motor A
    analogWrite(enB, data); // Send PWM signal to motor B
  }
}

void checkStatus()
{
  int readTemp, currentServo;
  sound0 = analogRead(vu0);
  sound0 = map(sound0, 0, 1023, 0, 99);
  sound1 = analogRead(vu1);
  sound1 = map(sound1, 0, 1023, 0, 99);
  sound2 = analogRead(vu2);
  sound2 = map(sound2, 0, 1023, 0, 99);
  power = analogRead(pow0);
  currentServo = 1;
  readTemp = Dynamixel.readTemperature(1);
  int temptemp = readTemp;
  if (temperature < readTemp)
  {
    temperature = readTemp;
    warmestServo = 1;
  }
  for (int i = 1; i < 5; i++)
  {
    currentServo = i * 10;
    readTemp = Dynamixel.readTemperature(currentServo);
    if (temperature < readTemp)
    {
      temperature = readTemp;
      warmestServo = currentServo;
    }
  }
}
