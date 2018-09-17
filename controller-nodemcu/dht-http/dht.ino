#include <DHT.h>

//DHT******************** 
DHT dht(pinDHT, DHT11); //DHT11, DHT22
//********************DHT 

void setup_dht(){
  dht.begin();
}
void loop_dht(){

  temp = dht.readTemperature();
  humi = dht.readHumidity();

  //======================
  // testdata ============
  if (isTest == 1) {
    temp = random(10,40);
    humi = random(10,60);
  }
  // testdata ============
  //======================
  
  // change noise data to 0
  if ( !isFloat(String(temp)) ) { 
    temp = 0;
    humi = 0;
  }
  
  //Json data generation ============================
  StaticJsonDocument<200> doc;
  JsonObject root = doc.to<JsonObject>();

  root["measuredt"] = "";       
  root["controller"] = "nodemcu";        
  root["sensor"] = "DHT";
  root["uptime"] = millis();
  root["temp"] = temp;
  root["humi"] = humi;
  root["ip"] = myIP.toString();
  
  serializeJson(root, jsonResult);
  serializeJson(root, Serial);
  Serial.println("");
  //============================Json data generation
}
//========================loop

