#include<ESP8266WiFi.h>
#include<DHT.h>
#include<ThingSpeak.h>

const char *ssid = "IIITS_Student";
const char *pass = "iiit5@2k18";

int DHTPIN = D3;

DHT dht(DHTPIN,DHT11);

WiFiClient client;
unsigned long ChannelNumber = 909529;
const char* WriteApi = "E1WONEC2U4WYAE3S";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(10);
  dht.begin();

  WiFi.begin(ssid,pass);
  ThingSpeak.begin(client);
  
  Serial.println("Connecting to :");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi Connected");
}

void loop() {
  // put your main code here, to run repeatedly:
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if(isnan(h) | isnan(t))
  {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  ThingSpeak.setField(1,t);
  ThingSpeak.setField(2,h);
  ThingSpeak.writeFields(ChannelNumber,WriteApi);
  
  Serial.println("Waiting...");
  delay(10000);  
}
