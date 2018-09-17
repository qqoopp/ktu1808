//Host Server config********************
char* ssid = gssid;
char* password = gpassword;
//********************Host Server config

void setup_http(){

    //connect to AP +++++++++++++++++++++
    WiFi.mode(WIFI_STA);
    delay(100);
    WiFi.begin( ssid, password );

    Serial.println();
    Serial.println();
    Serial.print("Wait for WiFi... ");

    while(WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }

    myIP = WiFi.localIP();

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(myIP);
    delay(10);
    //+++++++++++++++++++++connect to AP
}

void loop_http(){    
    if (jsonResult == "") return;
    
    Serial.print(myIP);
    Serial.print(" -> ");
    Serial.println(gatewayip);

    if(WiFi.status() == WL_CONNECTED) {
      if ( jsonResult != "" )  {
        sendhttp(jsonResult);
        jsonResult = "";
      }
    }
    Serial.print("wait ");
    Serial.println(" sec...");
}

//send data to server 
void sendhttp(String postdata){ 
  if (postdata == "") return; 
  String hosturl = "http://" + String(gatewayip) + ":" + String(port) + "/Postjson";
  
  HTTPClient http;
  http.begin(hosturl);
  //http.addHeader("POST /PostMeasure HTTP/1.1");
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Cache-Control","no-cache");
  http.POST(postdata);
  http.writeToStream(&Serial);
  String rtnmsg = http.getString();
  http.end();

  //Serial.println(rtnmsg);  
  Serial.print("posted");
  Serial.println(postdata);
}

