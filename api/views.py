from django.shortcuts import render
from django.http import JsonResponse
from . import models
import json

def sina_api(request):
    data = json.load(open("data/sina.json"))
    return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

def province(request):
    data = json.load(open("data/sina.json"))
    pro = eval(request.GET['province'])
    pro_num = 0
    for i in range(len(data['data']['list'])):
        if data['data']['list'][i]['name']==pro or data['data']['list'][i]['ename']==pro:
            pro_num = i
    dic = data['data']['list'][pro_num]
    dic.pop('hejian')
    for item in dic['city']:
        item.pop('citycode')
        item.pop('hejian')
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False})  
    
def country(request):
    data = json.load(open("data/sina.json"))
    country = eval(request.GET['country'])
    country_num = 0
    for i in range(len(data['data']['worldlist'])):
        if data['data']['worldlist'][i]['name']==country:
            country_num = i
    dic = data['data']['worldlist'][country_num]
    dic.pop('is_show_entrance')
    dic.pop('is_show_map')
    citycode = dic['citycode']
    data_country = json.load(open("data/country/"+citycode+".json"))
    city = data_country['data']['city']
    for i in range(len(city)):
        city[i].pop('is_show_entrance')
        city[i].pop('is_show_map')
    dic['city'] = city
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
    
def overall_China(request):
    data = json.load(open("data/sina.json"))
    dic = {}
    dic['times'] = data['data']['times']
    dic['mtime'] = data['data']['mtime']
    dic['gntotal'] = data['data']['gntotal']
    dic['deathtotal'] = data['data']['deathtotal']
    dic['sustotal'] = data['data']['sustotal']
    dic['curetotal'] = data['data']['curetotal']
    dic['econNum'] = data['data']['econNum']
    dic['heconNum'] = data['data']['heconNum']
    dic['asymptomNum'] = data['data']['asymptomNum']
    dic['jwsrNum'] = data['data']['jwsrNum']
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
    
def overall_world(request):
    data = json.load(open("data/sina.json"))
    dic = data['data']['othertotal']
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False}) 
    
def province_list(request):
    data = json.load(open("data/sina.json"))
    dic = data['data']['list']
    for i in range(len(dic)):
        dic[i].pop('city')
        dic[i].pop('hejian')
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False) 

def country_list(request):
    data = json.load(open("data/sina.json"))
    dic = data['data']['otherlist']
    for i in range(len(dic)):
        dic[i].pop('is_show_entrance')
        dic[i].pop('is_show_map')
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False)     
 
def history_China(request):
    data = json.load(open("data/sina.json"))
    data = data['data']['historylist']
    dic = {}
    dic['date'] = []
    dic['conadd'] = []
    dic['econNum'] = []
    dic['conNum'] = []
    dic['cureNum'] = []
    dic['deathNum'] = []
    dic['cureRate'] = []
    dic['deathRate'] = []
    n = len(data)
    for i in range(n-1,0,-1):
        dic['date'].append(data[i]['date'])
        dic['conadd'].append(data[i]['cn_conadd'])
        dic['econNum'].append(data[i]['cn_econNum'])
        dic['conNum'].append(data[i]['cn_conNum'])
        dic['cureNum'].append(data[i]['cn_cureNum'])
        dic['deathNum'].append(data[i]['cn_deathNum'])
        dic['cureRate'].append(data[i]['cn_cureRate'])
        dic['deathRate'].append(data[i]['cn_deathRate'])
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False) 
    
def history_world(request):
    data = json.load(open("data/sina.json"))
    data = data['data']['otherhistorylist']
    dic = {}
    dic['date'] = []
    dic['conadd'] = []
    dic['conNum'] = []
    dic['cureNum'] = []
    dic['deathNum'] = []
    n = len(data)
    for i in range(n-1,0,-1):
        dic['date'].append(data[i]['date'])
        dic['conadd'].append(data[i]['certain_inc'])
        dic['conNum'].append(data[i]['certain'])
        dic['cureNum'].append(data[i]['recure'])
        dic['deathNum'].append(data[i]['die']) 
    return JsonResponse(dic,json_dumps_params={'ensure_ascii':False},safe=False) 
    
def rate(request):
    data = json.load(open("data/sina.json"))
    data = data['data']['list']
    lis = []
    for i in range(len(data)):
        dic = {}
        dic['name'] = data[i]['name']
        dic['ename'] = data[i]['ename']
        x = 100.0*float(data[i]['cureNum'])/float(data[i]['value'])
        dic['cureRate'] = format(x,'.2f')
        x = 100.0*float(data[i]['deathNum'])/float(data[i]['value'])
        dic['deathRate'] = format(x,'.2f')
        lis.append(dic)
    return JsonResponse(lis,json_dumps_params={'ensure_ascii':False},safe=False) 

def continent(request):
    lis = []
    #to do
    continent_list = ['亚洲','欧洲','非洲','大洋洲','北美洲','南美洲']
    
    return JsonResponse(lis,json_dumps_params={'ensure_ascii':False},safe=False) 
'''
with open('history_China.json','w') as f:
    json.dump(dic,f,ensure_ascii=False)
'''    
    