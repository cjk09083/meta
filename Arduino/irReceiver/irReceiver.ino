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

void loop() {
  if (IrReceiver.decode()){
    Serial.println(IrReceiver.decodedIRData.command);
    IrReceiver.resume();
    return;                  
  }

  if(BT.available()>0){
    Serial.write(BT.read());  
  }

  delay(10);
}
