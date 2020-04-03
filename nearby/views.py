from django.shortcuts import render
from django.http import JsonResponse
from . import models
import math
def dist(lon1,lat1,lon2,lat2):
    radius=6371.004
    pi=math.pi
    lon1*=pi/180.0
    lat1*=pi/180.0
    lon2*=pi/180.0
    lat2*=pi/180.0
    tmp=math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2)
    return radius*math.acos(tmp)

def nearbyAsk(request):
    lon=eval(request.GET['lon'])
    lat=eval(request.GET['lat'])
    queryset=models.pois.objects.all()
    mindist=6371.0
    num1,num3,num5=0,0,0
    for x in queryset:
        tmpdist=dist(lon,lat,x.lon,x.lat)
        if(mindist>tmpdist):
            mindist=tmpdist
            minx=x
        if(tmpdist<1.0):
            num1+=1
            num3+=1
            num5+=1
        elif(tmpdist<3.0):
            num3+=1
            num5+=1
        elif(tmpdist<5.0):
            num5+=1
    mindist=round(mindist,2);
    return JsonResponse({'minDist':mindist,'location':minx.poiName,'num1':num1,'num3':num3,'num5':num5},json_dumps_params={'ensure_ascii':False})
