#include <ArduinoJson.h>

//values******************** 
int brate = 9600; 
float temp, humi;
String jsonResult = "";
int isTest = 1;   //1:test mode, 0:real mode
//********************values 

//GPIO******************** 
int pinDHT = 4;
//********************GPIO 

void setup(){
  
  setup_dht();  

  Serial.begin(brate);
}

void loop(){
  loop_dht();
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
