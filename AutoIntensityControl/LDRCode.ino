int LED = 2;
void setup() {
  // put your setup code here, to run once:  
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int  LDRValue = analogRead(A0);
  float brightness =255 - (LDRValue/3.92);
  analogWrite(LED,brightness);
  Serial.println(LDRValue);
  Serial.print("-->");
  Serial.print(brightness);
}
