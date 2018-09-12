#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

const int trigPin = 12;//D6
const int echoPin = 2; //D4
//12,14 
boolean setupwifi();
boolean connectUDP();
void signalLED(char);
 #define wifiname "Amith Kumar V"
 #define wifipass "amith1997"
  #define chipId="123" 
  unsigned int localPort = 7777;
  boolean wifiConnected=false;
  boolean udpConnected=false;
WiFiUDP UDP;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
char ReplyBuffer[] = "acknowledged"; // a string to send back

boolean setupwifi()
{
  WiFi.begin(wifiname,wifipass);
  Serial.println("connecting");
  while(WiFi.status()!=WL_CONNECTED)
  {
    Serial.println(".");
    delay(500);
    
  }
  Serial.println();
  Serial.println("connected");
  Serial.println(WiFi.localIP());
 return true; 
  }

  boolean connectUDP(){
boolean state = false;

Serial.println("");
Serial.println("Connecting to UDP");

if(UDP.begin(localPort) == 1){
Serial.println("Connection successful");
state = true;
}
else{
Serial.println("Connection failed");
}

return state;
}



void setup()
{
 
  Serial.begin(9600);
  wifiConnected=setupwifi();
  if(wifiConnected){
udpConnected = connectUDP();
if (udpConnected){

pinMode(12,OUTPUT);//D6 red
pinMode(14,OUTPUT);//D5 green
}
char value='0';
while(value=='0')
{
  if(wifiConnected)
  {

if(udpConnected)
{

// if there’s data available, read a packet
int packetSize = UDP.parsePacket();
digitalWrite(14,HIGH);
    digitalWrite(12,LOW);
    delay(1000);
     digitalWrite(14,LOW);
    digitalWrite(12,HIGH);
    delay(2000);
/*                                  if(packetSize==0)
{

    digitalWrite(12,HIGH);
    digitalWrite(14,LOW);
    delay(2000);
     digitalWrite(12,LOW);
    digitalWrite(14,HIGH);
    delay(1000);
}*/
if(packetSize)
{
Serial.println("");
Serial.print("Received packet of size ");
Serial.println(packetSize);
Serial.print("From ");
IPAddress remote = UDP.remoteIP();
for (int i =0; i < 4; i++)
{
Serial.print(remote[i], DEC);
if (i < 3)
{
Serial.print(".");
}
}
Serial.print(", port ");
Serial.println(UDP.remotePort());


UDP.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
Serial.println("Contents:");
value = packetBuffer[0];
Serial.println(value);


UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
UDP.write(ReplyBuffer);
UDP.endPacket();



}

delay(10);

}

}
}

 
}
}

void loop() {

if(wifiConnected){

if(udpConnected){

// if there’s data available, read a packet
int packetSize = UDP.parsePacket();
/*                                  if(packetSize==0)
{

    digitalWrite(12,HIGH);
    digitalWrite(14,LOW);
    delay(2000);
     digitalWrite(12,LOW);
    digitalWrite(14,HIGH);
    delay(1000);
}*/
if(packetSize)
{
Serial.println("");
Serial.print("Received packet of size ");
Serial.println(packetSize);
Serial.print("From ");
IPAddress remote = UDP.remoteIP();
for (int i =0; i < 4; i++)
{
Serial.print(remote[i], DEC);
if (i < 3)
{
Serial.print(".");
}
}
Serial.print(", port ");
Serial.println(UDP.remotePort());


UDP.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
Serial.println("Contents:");
char value = packetBuffer[0];
Serial.println(value);


UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
UDP.write(ReplyBuffer);
UDP.endPacket();
signalLED(value);


}
delay(10);

}

}
else
{
    
  
}

}



void signalLED(char value)
{
  if(value=='0')
  {
    digitalWrite(14,HIGH);
    digitalWrite(12,LOW);
    delay(1000);
     digitalWrite(14,LOW);
    digitalWrite(12,HIGH);
    
  }
  if(value=='1')
  { digitalWrite(12,LOW);
    digitalWrite(14,HIGH);
    
}


    
  
}
