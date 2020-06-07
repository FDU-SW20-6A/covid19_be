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

def dictError(lon,lat):
    return {
            'mapCenter':{'longitude':lon,'latitude':lat},
            'address':'error',
            'markers':[],
            'city':'error',
            'totalCase':0,
            'currentCase':0,
            'nearDis':-1,
            'nearLoc':'error',
            'case1':0,
            'case3':0,
            'case5':0,
        }

def myJsonResponse(ret):
    json_data=json.dumps(ret,ensure_ascii=False)
    response=HttpResponse(json_data)
    '''
    response['Access-Control-Allow-Origin']='http://127.0.0.1:8000'
    response['Access-Control-Allow-Methods']='POST,GET,OPTIONS'
    response['Access-Control-Max-Age']='2000'
    response['Access-Control-Allow-Headers']='*'
    '''
    return response

def isInputValid(lon,lat,citycode,markersNum):
    #valid longitude range:[73,136]
    #valid latitude range:[3,54]
    #valid markersNum range:>=1
    #valid citycode length:8
    lon*=1.0
    lat*=1.0
    if type(lon)!=float or lon<73 or lon>136:
        return False
    if type(lat)!=float or lat<3 or lat>54:
        return False
    if type(citycode)!=str or len(citycode)!=8:
        return False
    if type(markersNum)!=int or markersNum<1:
        return False
    return True

def nearbyAsk(lon,lat,citycode,markersNum):
    #response=urllib.request.urlopen('https://interface.sina.cn/news/wap/fymap2020_data.d.json')
    #sinaData=json.loads(response.read().decode('utf-8'))
    sinaData=json.load(open(r'data/sina.json','r',encoding='utf-8'))
    cityName,cityTotalNum,cityExistNum='unknown','unknown','unknown'
    for province in sinaData['data']['list']:
        for city in province['city']:
            if city['citycode']!='':
                provincecode=city['citycode'][:4]
                break
        if citycode[:4]!=provincecode:continue
        for city in province['city']:
            if city['citycode']=='' or city['citycode']!=citycode:continue
            cityName=city['mapName']
            cityTotalNum=city['conNum']
            cityExistNum=city['econNum']

    queryset=models.pois.objects.all()
    #print('querysetlength:',len(queryset))
    #markersNum=10 #更改此常量的值可以控制marker的数量

    mindist=[6371.0 for i in range(markersNum)]
    minx=[queryset[0] for i in range(markersNum)]

    num1,num3,num5=0,0,0
    for x in queryset:
        tmpdist=dist(lon,lat,x.lon,x.lat)

        for i in range(markersNum):
            if tmpdist<mindist[i]:
                for j in range(markersNum-1,i,-1):
                    mindist[j],minx[j]=mindist[j-1],minx[j-1]
                mindist[i],minx[i]=tmpdist,x
                break

        if tmpdist<1.0:
            num1+=1
            num3+=1
            num5+=1
        elif tmpdist<3.0:
            num3+=1
            num5+=1
        elif tmpdist<5.0:
            num5+=1
    mindist[0]=round(mindist[0],2);
    #return JsonResponse({'cityName':cityName,'cityTotalNum':cityTotalNum,'cityExistNum':cityExistNum,'isOversea':isOversea,'minDist':mindist,'location':minx.poiName,'num1':num1,'num3':num3,'num5':num5},json_dumps_params={'ensure_ascii':False})
    ret={
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
        }
    return myJsonResponse(ret)

def nearbyQueryAsk(request):
    input=request.GET
    lon=eval(input.get('lon','121.505236'))
    lat=eval(input.get('lat','31.300102'))
    citycode='CN'+input.get('citycode','310110')
    markersNum=eval(input.get('markersNum','10'))
    if not isInputValid(lon,lat,citycode,markersNum):
        return myJsonResponse(dictError(lon,lat))
    if citycode[:4] in {'CN50','CN11','CN31','CN12'}:citycode+='00000000'
    else:citycode=citycode[:6]+'0000000000'
    return nearbyAsk(lon,lat,citycode,markersNum)

def nearbyInitAsk(request):
    input=request.GET
    markersNum=eval(input.get('markersNum','10'))
    #print('markersNum:',markersNum)
    lon,lat=121.505236,31.300102
    citycode='CN31011000000000'
    if not isInputValid(lon,lat,'CN310110',markersNum):
        return myJsonResponse(dictError(lon,lat))
    return nearbyAsk(lon,lat,citycode,markersNum)
