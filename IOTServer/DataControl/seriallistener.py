#=========================================
# Listen from usb serial port and save data to log file
#=========================================

import serial
import time
import subprocess
import os
from time import strftime
from datetime import datetime
import json
import sys

serialbaudrate = 9600 # speed to get data from serial port
logfilepath = "./data/"
uptime = 0
tmpuptime = 0

def setSerial(ser, sensor, onoff):
    senddata = ("{\"sensor\":\"" + sensor + "\",\"onoff\":\"" + onoff + "\"}").encode('utf-8')
    print(senddata)
    ser.write(senddata)

def prompt(prompt):
    return input(prompt).strip()

##! genefate serial file
def putSerial(ser):
    #makes filename every min
    ymdhms = datetime.now().strftime('%Y%m%d%H%M%S.%f')
    ymdhm = ymdhms[:13] # max 20 digits limit( 8 digits for sec )
    filename = logfilepath +  ymdhm + ".log" 
    
    row = ser.readline()

    f = open(filename, 'ab')
    #if row[:1].decode('utf-8') == "{":
    if row[:1].decode('utf-8') == "{":
        #adddata = "{\"measuredt\":\"" + ymdhms + "\",\"data\":"
        adddata = row.decode('utf-8').replace("\"measuredt\":\"\"","\"measuredt\":\"" + ymdhms + "\"")
        f.write(adddata.encode('ascii'))
        #f.write(row)
    else:
        f.write(row)
    f.close()

def readIntent(ser):
    path = "./intent/" 
    for filename in os.listdir(path):  
        if filename.endswith(".log") and filename[0] !="@":
            f = open(path + filename, 'rb')
            rows = f.readlines()
            f.close()
            for row in rows:
                payload = row.strip()
                jdata = json.loads(payload)
                sensor = jdata.get("sensor")
                onoff = jdata.get("onoff")
                setSerial(ser,sensor,onoff)
                time.sleep(0.5)  # delay after intentet ordered
            os.rename(path + filename, path + "@" + filename)  #check trensferred data file

if __name__ == "__main__":
    #python -m serial.tools.list_ports
    portlist = subprocess.Popen(["python","-m","serial.tools.list_ports"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    print("currently connected ports list : ")
    #print(portlist.stdout.readlines().replace('\r\n', ''))
    for line in iter(portlist.stdout.readline, b''):
        print( line.strip().decode('utf-8') )
        print("")

    print("Present listner baudrate is : " + str(serialbaudrate))
    print("please sync arduino 'Serial.begin' baudrate " ) 

    comport = prompt("Input comport (ex)COM22): ")
    tmpserialbaudrate = prompt("Input baudrate (ex)9600): ")

    if tmpserialbaudrate != "":
        serialbaudrate = tmpserialbaudrate
   
    try:

        ser = serial.Serial(
            port=comport, 
            baudrate = serialbaudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0)

        print("Receiving data...")
        while(True):
            # uptime = time.time()
            # difftime = uptime - tmpuptime 
            # if ( difftime > 3.0 and difftime < 4.0 ):
            #     setSerial(ser,"led","on")
            # elif ( difftime > 6.0 ):
            #     setSerial(ser,"led","off")
            #     tmpuptime = uptime
            
            readIntent(ser)
            
            if (ser.inWaiting()>0):
                putSerial(ser)
            time.sleep(0.001)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    except serial.serialutil.SerialException as e:
        print('!!!Error : ' + str(e) )

    except:
        print("")
        print("Incoreect port. Please check port")
        exit