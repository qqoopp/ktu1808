#=========================================
# upload file data to db
#=========================================

import requests
import json
import time
import os
import sys

gatewayurl="http://127.0.0.1:8000/Postjson"
path = "./data/"

def checkdupfile(path,filename):
    for listfile in os.listdir(path):
        if (filename == listfile.replace("@","")):
            return False
    return True

try:
    while True:
        for filename in os.listdir(path):
            if filename.endswith(".log") and filename[0] !="@":

                f = open(path + filename, 'rb')
                rows = f.readlines()
                f.close()

                #check duplicated file 
                if checkdupfile(path,filename):
                    os.rename(path + filename, path + "@" + filename)  #add @ to filename
                else:
                    newfilename = filename.replace(".log","1.log")
                    os.rename(path + filename, path + "@" + newfilename)  #add @ and 1 to filename
                
                for row in rows:
                    payload = row.strip() #trim
                    response = requests.post(gatewayurl, payload)
                    #response = requests.post(url,  data=json.dumps(payload))
                    #print(response.text) #TEXT/HTML
                    time.sleep(1) #send data every 1sec
        time.sleep(1) 

except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

except:
    #print(response)
    print("upload failed!")