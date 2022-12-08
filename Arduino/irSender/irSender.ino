#include <IRremote.hpp>
// #include <IRremote.h>
// #include <IRremoteInt.h>

// IrSender irsender;
int val[10];
int pinGap = 8;
int adcRef = 14 - pinGap;
int mval = 0;
String cmdStr[2][3][3] = {
  {
    {"A", "Z", "X"},
    {"B", "3", "G"},
    {"Select", "End", "E"}
  },
  {
    {"Start", "MR", "Mute"},
    {"ML", "Up", "Down"},
    {"Right", "Left", "Power"}
  }
};

int cmdHex[2][3][3] = {   //          224       311       369
  {
    {0x54, 0x44, 0x43},   // A0 - D8   A        Z         X
    {0x53, 0x40, 0x42},   // A0 - D9   B        3         G
    {0x52, 0x23, 0x41}    // A0 - D10  Select   End       E
  },   
  {
    {0x51, 0x32, 0x31},   // A1 - D8   Start    Mute_R    Mute
    {0x30, 0x21, 0x22},   // A1 - D9   Mute_L   Up        Down
    {0x24, 0x23, 0x10}    // A1 - D10  Right    Left      Power
  }
};

void setPin(int num, int val);
void getVolt(int num);
void getMag(int num);

void sendMsg(int num, int pin, int val);
void chkValue(int num, int pin, int val);

void setup() {
  Serial.begin(115200);
  IrSender.begin(2);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  setPin(4, 1);   // IR
  setPin(3, 0);   // Run
  setPin(5,1);    // Err
  setPin(8, 0);
  setPin(9, 0);
  setPin(10, 0);
}

void loop() {
  getMag(A2);
  getVolt(A0);
  getVolt(A1);
//  for (int i = 0; i < 3; i++) {
//    sendMsg(0, 0, 1);
//    delay(5);
//  }
  //  delay(10);
  //  sendMsg(0, 1);

  Serial.println();
  delay(10);
//  delay(250);
}


void setPin(int num, int val) {
  // pinMode(adc, INPUT);
  pinMode(num, OUTPUT);
  digitalWrite(num, val);
}

void getMag(int num) {
  mval = analogRead(num);
  Serial.print("M:");
  Serial.print(mval);
  Serial.print(" ");
}

void getVolt(int adc) {
  // int adc = adcRef + num;
  digitalWrite(8, HIGH);
  delay(10);
  // val[num] = analogRead(adc);
  int adc1 = analogRead(adc);
  digitalWrite(8, LOW);

  digitalWrite(9, HIGH);
  delay(10);
  int adc2 = analogRead(adc);
  digitalWrite(9, LOW);

  digitalWrite(10, HIGH);
  delay(10);
  int adc3 = analogRead(adc);
  digitalWrite(10, LOW);

  Serial.print("A");
  Serial.print(adc - 14);
  Serial.print(":");
  Serial.print(adc1);
  chkValue(adc - 14, 0, adc1);
  Serial.print(", ");
  Serial.print(adc2);
  chkValue(adc - 14, 1, adc2);
  Serial.print(", ");
  Serial.print(adc3);
  chkValue(adc - 14, 2, adc3);
  // chkValue(num-3,val[num]);
  Serial.print(" ");
}

void chkValue(int num, int pin, int val) {
  int setArr[] = {100, 100, 100};
  if (val < 10) return;  
  else if (val < 300) setArr[0] = 0;
  else if (val < 350) setArr[0] = 1;
  else if (val < 400) setArr[0] = 2;
  else if (val < 430) setArr[0] = 0, setArr[1] = 1;
  else if (val < 475) setArr[0] = 0, setArr[1] = 2;
  else if (val < 500) setArr[0] = 1, setArr[1] = 2;
  else setArr[0] = 0, setArr[1] = 1, setArr[2] = 2;

  // 0 = 225, 1 = 314, 2= 370
  // 0 + 1 = 419, 0 + 2 = 458, 1 + 2 = 498
  // 0 + 1 + 2 = 550

  Serial.print(" {");
  for (int i = 0; i <= 2; i++ ) {
    int set = setArr[i];
    if (set > 10 ) break;
    Serial.print(" ");
    Serial.print(set);
    Serial.print(cmdStr[num][pin][set]);
    sendMsg(num, pin, set);
    Serial.print(",");
    delay(50);
  }
  Serial.print("} ");
}

void sendMsg(int num, int pin, int set) {
  digitalWrite(5, 0);
  uint16_t sAddress = 0x0102; // 0x0102
  uint8_t sCommand = cmdHex[num][pin][set];
  uint8_t sRepeats = 3;
//  Serial.print(sCommand, HEX);
//  Serial.print(sCommand);
  int type = 2;     // [NEC, Sony, RC5, RC6]
  
  switch(type){
    case 2: 
        IrSender.sendSony(sAddress, sCommand, sRepeats);              
        break;  
    case 3:  
        IrSender.sendRC5(sAddress, sCommand, sRepeats);              
        break;  
    case 4:  
        IrSender.sendRC6(sAddress, sCommand, sRepeats);              
        break;
    default:  
        IrSender.sendNEC(sAddress, sCommand, sRepeats);
  }  
  
  digitalWrite(5, 1);
  //  IrSender.sendNEC(0xa90,32);

}
