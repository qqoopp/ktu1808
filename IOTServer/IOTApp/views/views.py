from django.shortcuts import render
import json
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from IOTApp.models import *
from django.utils import timezone
from datetime import datetime
import http
from django.http import HttpResponse

import requests
import time
import urllib.request

def getMyIP():
    ipaddresss = tMyServerinfo.objects.values('IPaddress')
    for ipaddress in ipaddresss:
        return ipaddress["IPaddress"]

def getDatastoreIP():
    ipaddresss = tMyServerinfo.objects.values('DatastoreIPaddress')
    for ipaddress in ipaddresss:
        return ipaddress["DatastoreIPaddress"]

#===============================
# save json data to db
#===============================
#@csrf_protect
@csrf_exempt
def Postjson(request): 
    if request.method=="POST":

        try:
            bodydata = request.body.decode("utf-8").replace('\n', '').replace('\r', '').replace(' ', '')
            jdata = json.loads(bodydata)
            
        except Exception as e:
            return StreamingHttpResponse("err1: " + str(request.body))

        rdt = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S.%f")
        rdt2 = timezone.localtime().strftime("%Y%m%d%H%M%S.%f")
        ControllerNo = jdata.get("controller").upper()
        SensorNo = jdata.get("sensor").upper()

        if ( jdata.get("measuredt") == ""):
            bodydata = bodydata.replace("\"measuredt\":\"\"","\"measuredt\":\"" + rdt2 + "\"")

        controllerip = jdata.get("ip")
        ipaddress = ""
        mydevice = 0
        ipaddresss = tDevice.objects.filter(DeviceNo=ControllerNo).values('IPaddress')
        ipaddresss2 = tDevice.objects.filter(DeviceNo=SensorNo).values('IPaddress')
        mydevices = tMyServerinfo.objects.values('DeviceSeq')[:1]

        #update controller ip
        for ipaddress in ipaddresss:
            if controllerip != ipaddress:
                tDevice.objects.filter(DeviceNo=ControllerNo).update(IPaddress=controllerip)

        #update sensor ip( controller ip )
        for ipaddress in ipaddresss2:
            if controllerip != ipaddress:
                tDevice.objects.filter(DeviceNo=SensorNo).update(IPaddress=controllerip)

        ordercd = ""

        for keyval in jdata.keys():
            if keyval.upper() == "ordercd".upper():
                ordercd = jdata.get(keyval).upper()

        curordercds = tDevice.objects.filter(DeviceNo=SensorNo).values('StatusCd')
        for curordercd in curordercds:
            curordercd = curordercd

        try:
            #update ordercd to device
            if (ordercd != ""):
                # f = open("a.txt","a")
                # f.write(str(ordercd))                
                tDevice.objects.filter(DeviceNo=SensorNo).update(StatusCd=ordercd,UptDT= rdt)

            #if ordercd is off stop measuring
            if (curordercd != "OFF") or (ordercd != ""):
                postdata = tMeasure(
                    MeasureDT = rdt2,#jdata.get('measuredt'),
                    ControllerNo = ControllerNo,
                    SensorNo = SensorNo,
                    OrderCd = ordercd, #on/off
                    RcvDT = rdt,
                    Value = bodydata,
                )
                postdata.save()

        except Exception as e:
            #return StreamingHttpResponse("err2: " + str(e))#str(request.body))
            return StreamingHttpResponse("err2: " + str(request.body))

        return StreamingHttpResponse(str(request.body))
        #return HttpResponse(status=200)
    
    return StreamingHttpResponse("GET")

#===============================
# Trans data to server
#===============================
@csrf_exempt
def Transdata(request):
    if request.method=="POST":
        url="http://" + getDatastoreIP() + "/Postjson"

        # read table rows. update senddata
        rdata = tMeasure.objects.all().filter(SndDT__isnull=True)[:1]

        try:
            for row in rdata:
                payload = row.Value.strip()
                response = requests.post(url, payload)
                time.sleep(0.1)

                rdt = timezone.localtime().strftime("%Y%m%d%H%M%S.%f")
                tMeasure.objects.filter(id=row.id).update(SndDT=rdt)

        except Exception as e:
            return StreamingHttpResponse("err: " + str(request.body))

        return StreamingHttpResponse(str(request.body))
        #return HttpResponse(str(request.body))

    return StreamingHttpResponse("GET")


#===============================
# gateway control
#===============================
@csrf_exempt
def PostController(request, selected, onoff):   # on/off
    #if request.method=="POST":

    masters = tDevice.objects.filter(DeviceSeq__in=selected)

    reqno = ""
    for master in masters:      
        sensor = master.DeviceNo
    
    url = "http://192.168.137.209/Intentjson?"  #gateway
    payload = '"controller":"NodeMcU","sensor":"led","onoff":"on"'
    

    response = requests.post(url, payload)
    #data = json.dumps(post_fields).encode('utf8')
    #urllib.request.urlopen(url,data=data)
    #return 0#render(request,'tDevice')

    return StreamingHttpResponse(response)