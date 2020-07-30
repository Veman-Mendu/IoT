#include<SPI.h>
#include<MFRC522.h>

#define IR_Pin      2
#define RST_Pin     9
#define SDA         10

MFRC522 mfrc522(SDA,RST_Pin);

void setup() {
  // put your setup code here, to run once:
  pinMode(IR_Pin,INPUT);
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(7,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(IR_Pin) == HIGH){
    Serial.println("OBJECT is Present");
    delay(2000);
    rfid();
  }
  else{
    Serial.println("No OBJECT");
    delay(2000);
  }
}


void rfid(){
  if(mfrc522.PICC_IsNewCardPresent()){
      if(mfrc522.PICC_ReadCardSerial()){
        Serial.print("UID : ");
    
        String ID = "";
        for (byte i = 0; i < mfrc522.uid.size; i++){
          ID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
          ID.concat(String(mfrc522.uid.uidByte[i],HEX));
      
          Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
          Serial.print(mfrc522.uid.uidByte[i],HEX);
        }
         if(ID.substring(1) == bluetooth.read()){
          Serial.println("");
          Serial.println("Access Granted");
          digitalWrite(7,HIGH);
          delay(2000);
         }
         else{
          Serial.println("Access Denied");
          digitalWrite(7,LOW);
          delay(2000);
        }  
      }
    }
    else{
      //Send message to SECURITY
    }
}
