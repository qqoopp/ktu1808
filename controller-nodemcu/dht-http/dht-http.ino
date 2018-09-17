#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

//http==============================
char* gssid  = "AP-00";
char* gpassword = "12345678";
char* gatewayip = "192.168.137.1";//pc
const uint16_t port = 8000;
IPAddress myIP;
//==============================http

//values******************** 
int brate = 9600; 
float temp, humi;
String jsonResult = "";
int isTest = 0;   //1:test mode, 0:real mode
//********************values 

//GPIO******************** 
int pinDHT = D4;
//********************GPIO 

void setup(){
  
  setup_dht();  

  Serial.begin(brate);
  setup_http();  
}

void loop(){
  loop_dht();
  loop_http(); 
  delay(3000);
}


//isFloat=========================
//check whether tString is numeric or not ( to filter noise data  )
//====================================
boolean isFloat(String tString) {
  String tBuf;
  boolean decPt = false;
  
  if(tString.charAt(0) == '+' || tString.charAt(0) == '-') tBuf = &tString[1];
  else tBuf = tString;  

  for(int x=0;x<tBuf.length();x++)
  {
    if(tBuf.charAt(x) == '.') {
      if(decPt) return false;
      else decPt = true;  
    }    
    else if(tBuf.charAt(x) < '0' || tBuf.charAt(x) > '9') return false;
  }
  return true;
}
//=========================isFloat
