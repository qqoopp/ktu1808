#=========================================
# Listen from usb serial port and save data to log file
#=========================================

import time
import os
from time import strftime
from datetime import datetime
import sys

logfilepath = "./data/"

try:
    while True:
        ymdhms = datetime.now().strftime('%Y%m%d%H%M%S.%f')
        ymdhm = ymdhms[:12]#datetime.now().strftime('%Y%m%d%H%M')
        filename = logfilepath +  ymdhm + ".log" 

        rowdata = '{"measuredt":"","controller":"Arduino","sensor":"TMP","uptime":4000,"temp":163.8672}\n'

        f = open(filename, 'ab')

        if rowdata[:1] == "{":
            rowdata = rowdata.replace("\"measuredt\":\"\"","\"measuredt\":\"" + ymdhms + "\"")
            f.write(rowdata.encode('ascii'))
        else:
            f.write(rowdata.encode('ascii'))
        f.close()

        time.sleep(2)

except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
