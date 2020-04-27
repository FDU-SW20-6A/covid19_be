from django.shortcuts import render
from django.http import HttpResponse
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

def nearbyAsk(lon,lat,citycode):
    #response=urllib.request.urlopen('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    #sinaData=json.loads(response.read().decode('utf-8'))
    sinaData=json.load(open(r'data/sina.json','r',encoding='utf-8'))
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
    markersNum=10 #更改此常量的值可以控制marker的数量

    mindist=[6371.0 for i in range(markersNum)]
    minx=[queryset[0] for i in range(markersNum)]

    num1,num3,num5=0,0,0
    for x in queryset:
        tmpdist=dist(lon,lat,x.lon,x.lat)

        for i in range(markersNum):
            if(tmpdist<mindist[i]):
                for j in range(markersNum-1,i,-1):
                    mindist[j],minx[j]=mindist[j-1],minx[j-1]
                mindist[i],minx[i]=tmpdist,x
                break

        if(tmpdist<1.0):
            num1+=1
            num3+=1
            num5+=1
        elif(tmpdist<3.0):
            num3+=1
            num5+=1
        elif(tmpdist<5.0):
            num5+=1
    mindist[0]=round(mindist[0],2);
    #return JsonResponse({'cityName':cityName,'cityTotalNum':cityTotalNum,'cityExistNum':cityExistNum,'isOversea':isOversea,'minDist':mindist,'location':minx.poiName,'num1':num1,'num3':num3,'num5':num5},json_dumps_params={'ensure_ascii':False})
    json_data=json.dumps({
            'mapCenter':{'longitude':lon,'latitude':lat},
            'address':cityName,
            'markers':[{'position':{'longitude':minx[i].lon,'latitude':minx[i].lat},'title':minx[i].poiName}for i in range(markersNum)],
            'city':cityName,
            'totalCase':cityTotalNum,
            'currentCase':cityExistNum,
            'nearDis':mindist[0],
            'nearLoc':minx[0].poiName,
            'case1':num1,
            'case3':num3,
            'case5':num5,
        },
        ensure_ascii=False
        )
    response=HttpResponse(json_data)
    response['Access-Control-Allow-Origin']='*'
    response['Access-Control-Allow-Methods']='POST,GET,OPTIONS'
    response['Access-Control-Max-Age']='2000'
    response['Access-Control-Allow-Headers']='*'
    return response

def nearbyQueryAsk(request):
    lon=eval(request.GET['lon'])
    lat=eval(request.GET['lat'])
    citycode='CN'+request.GET['citycode']
    if(citycode[:4]=='CN50' or citycode[:4]=='CN11' or citycode[:4]=='CN31' or citycode[:4]=='CN12'):citycode+='00000000'
    else:citycode=citycode[:6]+'0000000000'
    return nearbyAsk(lon,lat,citycode)

def nearbyInitAsk(request):
    lon,lat=121.505236,31.300102
    citycode='CN31011000000000'
    return nearbyAsk(lon,lat,citycode)
