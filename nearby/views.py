from django.shortcuts import render
from django.http import JsonResponse
from . import models
import math
import json
import urllib.request

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
    citycode='CN'+request.GET['citycode']
    citycode=citycode[:6]+'0000000000'

    #response=urllib.request.urlopen('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    #sinaData=json.loads(response.read().decode('utf-8'))
    sinaData=json.load(open(r'data\sina.json','r',encoding='gbk'))
    cityName='unknown'
    cityTotalNum='unknown'
    cityExistNum='unknown'
    isOversea=0
    for province in sinaData['data']['list']:
        for city in province['city']:
            if(city['citycode']!=''):
                provincecode=city['citycode'][:4]
                break
        if(citycode[:4]!=provincecode):continue
        for city in province['city']:
            if(city['citycode']=='' or city['citycode']!=citycode):continue
            cityName=city['mapName']
            cityTotalNum=city['conNum']
            cityExistNum=city['econNum']
            if(city['jwsr']==''):isOversea=0
            else:isOversea=1
    

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
    return JsonResponse({'cityName':cityName,'cityTotalNum':cityTotalNum,'cityExistNum':cityExistNum,'isOversea':isOversea,'minDist':mindist,'location':minx.poiName,'num1':num1,'num3':num3,'num5':num5},json_dumps_params={'ensure_ascii':False})
