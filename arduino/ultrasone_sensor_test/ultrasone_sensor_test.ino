const int trigger = 4;
const int echo = 2;
long tijd;
//int afstand

void setup() {
  pinMode(trigger,OUTPUT);
  pinMode(echo, INPUT);
  digitalWrite(trigger, 0);
  Serial.begin(9600);
  DDRB = 0x3F;

}

void loop() {

  Serial.print("afstand in cm: ");
  Serial.println(afstand(trigger, echo));
  //Serial.print("De gemiddelde afstand over 6 metingen: ");
  //Serial.println(afstandAVGprecies(trigger, echo));
  Serial.println();
  //vumeter(afstand(trigger,echo));
  delay(0.1);
}

int afstand(int trigger, int echo){
  digitalWrite(trigger, 1);
  delayMicroseconds(10);
  digitalWrite(trigger, 0);
  tijd = pulseIn(echo, 1);
//  if ((tijd * 0.0343 / 2) > 250) {
//    return -1;
//  }
  return tijd * 0.0343 / 2;
}

int afstandAVGprecies(int trigger, int echo){
  int afstandAVG[6];
  int afs;
  int countAfstand;
  for (int i = 0; i < 6; i++){
    digitalWrite(trigger, 1);
    delayMicroseconds(10);
    digitalWrite(trigger, 0);
    tijd = pulseIn(echo, 1);
    afs = tijd * 0.0343 / 2;
    afstandAVG[i] = afs;
  }
  for (int i = 0; i < 6; i++){
    countAfstand += afstandAVG[i];
  }
    countAfstand = countAfstand - getMax(afstandAVG) - getMin(afstandAVG);
    return countAfstand / 4;
}

int getMax(int afstandarray[6]){
  int mxm;
  mxm = afstandarray[0];
  for (int i = 0; i < 6; i++) {
    if (afstandarray[i]>mxm) {
    mxm = afstandarray[i];
    }
  }
return mxm;
}

int getMin(int afstandarray[6]){
  int mn;
  mn = afstandarray[0];
  for (int i = 0; i < 6; i++) {
    if (afstandarray[i]<mn) {
      mn = afstandarray[i];
    }
  }
return mn;
}

void vumeter (int afstand){
  int result;
  result = map(afstand, 0, 60, 0, 6);
  if (pow(2,result) == 2){
    result = 2;
  }
  if (afstand > 60){
    result = 6;  
  }

  if (afstand == -1){
    for (int i = 0; i < 10; i++){
      PORTB = B111111;
      delay(50);
      PORTB = B000000;
      delay(50);
    } 
  }
  Serial.println(afstand);
  Serial.println(result);
  PORTB = pow(2,result);
}

