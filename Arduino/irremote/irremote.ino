#include <IRremote.h>
#include <IRremoteInt.h>
#include <SoftwareSerial.h>
SoftwareSerial BT(4,3);

int RECV_PIN = 2;
String dir = "err";

void setup() {
  Serial.begin(115200);
  BT.begin(9600);
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);

}

void dump(int val) {
  Serial.print(val);
  switch (val) {
    case 64:
      dir = "up";
      break;
    case 67:
      dir = "right";
      break;
    case 66:
      dir = "left";
      break;
    case 65:
      dir = "down";
      break;
    case 68:
      dir = "enter";
      break;
    default:
      dir = "err";
      break;
  }

  if(val==0) return;
  Serial.print(" (");
  Serial.print(dir);
  BT.println(dir);
  Serial.print(")");
  Serial.println();
}

void loop() {
  if (IrReceiver.decode()){
//    Serial.println(IrReceiver.decodedIRData.command);
    dump(IrReceiver.decodedIRData.command);
    IrReceiver.resume();
    return;                  
  }

  if(BT.available()>0){
    Serial.write(BT.read());  
  }

  delay(10);
}
