#include <IRremote.hpp>
// #include <IRremote.h>
// #include <IRremoteInt.h>

// IrSender irsender;
int val[10];
int adcRef = 14 - 3;
String cmdStr[][3] = {
                    {"home","up","left"},
                    {"enter","right","down"}
                  };

int cmdHex[][3] = {
                    {0x45,0x40,0x42},
                    {0x44,0x43,0x41}
                  };

void setPin(int num);
void getVolt(int num);
void sendMsg(int num, int val);
void chkValue(int num, int val);

void setup() {
  Serial.begin(115200);
  IrSender.begin(2);
  setPin(3);
  setPin(4);
}

void loop() {
  getVolt(3);
  getVolt(4);
  
  Serial.println();
  delay(250);
}

void setPin(int num){
  int adc = adcRef + num;
  pinMode(adc, INPUT);
  pinMode(num, OUTPUT);
  digitalWrite(num, LOW); 
}

void getVolt(int num){
  int adc = adcRef + num;
  digitalWrite(num, HIGH); 
  delay(10);
  val[num] = analogRead(adc);
  digitalWrite(num, LOW);
  Serial.print("A");
  Serial.print(num-3);
  Serial.print(":");
  Serial.print(val[num]);
  chkValue(num-3,val[num]);
  Serial.print(" ");
}

void chkValue(int num, int val){
  int setArr[] = {100,100,100};
  if(val < 10) return;
  else if(val < 200) setArr[0] = 0;
  else if(val < 250) setArr[0] = 1;
  else if(val < 290) setArr[0] = 2;
  else if(val < 320) setArr[0] = 0, setArr[1] = 1;
  else if(val < 350) setArr[0] = 0, setArr[1] = 2;
  else if(val < 390) setArr[0] = 1, setArr[1] = 2;
  else setArr[0] = 0, setArr[1] = 1, setArr[2] = 2;
  Serial.print(" {");
  for (int i=0; i <= 2; i++ ){
    int set = setArr[i];
    if(set > 10 ) break;
    // Serial.print(" ");
    // Serial.print(set); 
    // Serial.print(cmdStr[num][set]);
    sendMsg(num,set);
    Serial.print(",");
    delay(10);
  }
  Serial.print("} ");
}

void sendMsg(int num, int set){
  
  uint16_t sAddress = 0xC0DA;
//  if(num==0 && set ==0) sAddress = 0x4;
  uint8_t sCommand = cmdHex[num][set];
  uint8_t sRepeats = 0;
  Serial.print(sCommand,HEX);
  IrSender.sendNEC(sAddress, sCommand, sRepeats);
  // irsender.sendNFC(0xa90,32);

}
