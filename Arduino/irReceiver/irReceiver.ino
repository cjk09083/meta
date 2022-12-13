#include <IRremote.h>
#include <IRremoteInt.h>

int RECV_PIN = 2;
String dir = "err";
int storage = 0;
long input_ms = 0;

void setup() {
  Serial.begin(115200);
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
  delay(100);
}

void loop() {
  if (IrReceiver.decode()){
    if (IrReceiver.decodedIRData.flags & IRDATA_FLAGS_WAS_OVERFLOW) {
//        Serial.println(F("Overflow detected"));
        Serial.println("0");
    } else {
      int cmd = IrReceiver.decodedIRData.command;
//      if (cmd > 100) {Serial.print("Over!! "); }
//      if (cmd < 1) {Serial.print("Zero!! "); }
      if(0 < cmd && cmd < 100){
  //      IrReceiver.printIRResultRawFormatted(&Serial, true);  // Output the results in RAW format
  //      IrReceiver.compensateAndPrintIRResultAsCArray(&Serial, true); // Output the results as uint8_t source code array of ticks
  //      IrReceiver.printIRResultShort(&Serial);
//        Serial.print("( ");
//        Serial.print(cmd,HEX);
//        Serial.print(" ) => ");
          long duration = millis() - input_ms;
          if((cmd != storage)|| duration > 50){
//            Serial.print(duration);
//            Serial.print(":");
            Serial.println(cmd);
            input_ms= millis();
          }
          storage = cmd;
      }
//      else{Serial.println(cmd);}
      IrReceiver.resume();
      
      return;         
    }   
  }
  delay(1);
}


//#include <IRremote.h>
//#include <IRremoteInt.h>
//
//IRrecv energen(2);
//decode_results results;
//
//void setup() {
//  Serial.begin(115200);
//  energen.enableIRIn();
//}
//
//void loop() {
//  if(energen.decode(&results)){
//    Serial.println(results.value,DEC);
//    energen.resume();
//  }
//}
