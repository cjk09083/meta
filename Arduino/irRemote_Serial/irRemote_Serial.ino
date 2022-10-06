#include<IRremote.h>
int IRPIN = 2;
IRrecv irDetect(IRPIN); // 'irDetect'라는 이름으로 수신객체 생성
decode_results irIn; //값이 저장 되는 클래스객체(decode_res...)의 이름(irln)선언

void setup() {
  Serial.begin(9600);
  irDetect.enableIRIn();  // 수신 시작  
}
void loop() {
  if (irDetect.decode(&irIn)) {   //수신된 값이 있다면 
    Serial.println(irIn.value, HEX);  // 값을 시리얼창으로 출력
    irDetect.resume();     // 다음 값 받기
  }
  delay(100); // 100ms 마다 수신 & 수신 에러 방지
}
