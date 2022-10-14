int input1=A0;

int output1=13;
int output2=12;
int output3=11;
int output4=10;
int output5=9;
int output6=8;

void setPin(int num);
void getVolt(int num);

int val[20];

void setup()
{
  Serial.begin(115200);
  pinMode(input1, INPUT);
  setPin(output1);
  setPin(output2);
  setPin(output3);
  setPin(output4);
  setPin(output5);
  setPin(output6);
}

void loop()
{
  getVolt(output1);
  getVolt(output2);
  getVolt(output3);
  getVolt(output4);
  getVolt(output5);
  getVolt(output6);
  
  Serial.println();
  delay(250);
}



void setPin(int num){
  // pinMode(adc, INPUT);
  pinMode(num, OUTPUT);
  digitalWrite(num, LOW); 
}

void getVolt(int num){
  digitalWrite(num, HIGH); 
  delay(10);
  val[num] = analogRead(input1);
  digitalWrite(num, LOW);
  Serial.print("D");
  Serial.print(num);
  Serial.print(":");
  Serial.print(val[num]);
  Serial.print(" ");
}
