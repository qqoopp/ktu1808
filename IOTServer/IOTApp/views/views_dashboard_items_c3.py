from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from IOTApp.models import tMeasure, tRouting
import json

maxdatarows = 100
maxtablerows = 10
maxgauagerows = 1


@login_required(login_url='/admin/login/')
@csrf_exempt
def chart_line_c3(request,qsensor):

    qsensor = qsensor.upper()
    rowcnt = int(tMeasure.objects.filter(SensorNo=qsensor).count())

    sensordata = ""
    columns = ""

    try:
        if rowcnt == 0:
            sensordata = ""
        else:
            sensordata = tMeasure.objects.filter(SensorNo=qsensor).order_by('-MeasureDT').values('Value')[:maxdatarows]
            columns = list(json.loads(sensordata[0]['Value']).keys())
            columns.remove('measuredt')
            columns.remove('controller')
            columns.remove('sensor')
            columns.remove('uptime')
            columns.remove('ip')
    except:
        pass

    return render(request,'IOTApp/chart_line_c3.html',{'sensordata':sensordata,'columns':columns})

@login_required(login_url='/admin/login/')
@csrf_exempt
def chart_guage_c3(request,qsensor):

    qsensor = qsensor.upper()
    rowcnt = int(tMeasure.objects.filter(SensorNo=qsensor).count())

    sensordata = ""
    columns = ""

    try:
        if rowcnt == 0:
            sensordata = ""
        else:
            sensordata = tMeasure.objects.filter(SensorNo=qsensor).order_by('-MeasureDT').values('Value')[:maxgauagerows]
            columns = list(json.loads(sensordata[0]['Value']).keys())
            columns.remove('measuredt')
            columns.remove('controller')
            columns.remove('sensor')
            columns.remove('uptime')
            columns.remove('ip')        
    except:
        pass

    return render(request,'IOTApp/chart_guage_c3.html',{'sensordata':sensordata,'columns':columns})

@login_required(login_url='/admin/login/')
@csrf_exempt
def chart_guage2_c3(request,qsensor):

    qsensor = qsensor.upper()
    rowcnt = int(tMeasure.objects.filter(SensorNo=qsensor).count())

    sensordata = ""
    columns = ""

    try:
        if rowcnt == 0:
            sensordata = ""
        else:
            sensordata = tMeasure.objects.filter(SensorNo=qsensor).order_by('-MeasureDT').values('Value')[:maxgauagerows]
            columns = list(json.loads(sensordata[0]['Value']).keys())
            columns.remove('measuredt')
            columns.remove('controller')
            columns.remove('sensor')
            columns.remove('uptime')
            columns.remove('ip')
    except:
        pass            

    return render(request,'IOTApp/chart_guage2_c3.html',{'sensordata':sensordata,'columns':columns})


@login_required(login_url='/admin/login/')
@csrf_exempt
def chart_scatter_c3(request,qsensor):

    qsensor = qsensor.upper()
    rowcnt = int(tMeasure.objects.filter(SensorNo=qsensor).count())

    sensordata = ""
    columns = ""

    try:
        if rowcnt == 0:
            sensordata = ""
        else:
            sensordata = tMeasure.objects.filter(SensorNo=qsensor).order_by('-MeasureDT').values('Value')[:maxdatarows]
            columns = list(json.loads(sensordata[0]['Value']).keys())
            columns.remove('measuredt')
            columns.remove('controller')
            columns.remove('sensor')
            columns.remove('uptime')
            columns.remove('ip')
    except:
        pass

    return render(request,'IOTApp/chart_scatter_c3.html',{'sensordata':sensordata,'columns':columns})