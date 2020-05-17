# coding=utf-8
import requests
import json
import datetime
import time
import random

country_code = ['SCIT0039','SCUS0001','SCKR0082','SCIR0098','SCJP0081','SCFR0033','SCDE0049','SCES0034']
country_list = ["意大利","美国","韩国","伊朗","日本","法国","德国","西班牙"]
fail_tot = 0

def get_data(url,filename):
    
    limit = 3
    t = 0
    while (t<limit):
        with requests.get(url) as r:
            if r.status_code == 200:
                data = r.json()  
                try :
                    with open(filename,'w',encoding='utf-8') as f:
                        json.dump(data,f,ensure_ascii=False)
                except :
                    with open(filename,'w',encoding='utf-8') as f:
                        f.write(str(data))
                break
            else:
                t = t+1
                time.sleep(0.5)
        if t==limit: print(url,' fail') 
    return
    
    
def get_sina_api():

    url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json'
    filename = 'data/sina.json'    
    get_data(url,filename)

    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['otherlist']   
    
    for i in range(len(country_list)): 
        #name = dic[i]['name']
        #citycode = dic[i]['citycode']
        citycode = country_list[i]
        url = 'https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode='+citycode
        filename = 'data/country/'+citycode+'.json'
        if citycode!='': get_data(url,filename)

def continent():
    # 添加现存确诊

    continent_list = ['亚洲','欧洲','非洲','大洋洲','北美洲','南美洲','其它']
    con = json.load(open('data/continent.json',encoding='utf-8'))
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['worldlist']
    ans = [{} for i in range(7)]
    for i in range(len(continent_list)):
        sum = [0 for j in range(9)]
        ans[i]['country'] = []
        for j in range(len(dic)): 
            name = dic[j]['name']
            #If a new country appears, but we don't know which continent it belongs to, ignore it
            if name in con and con[name]==continent_list[i]:
                cdic = {}
                if name=='中国':
                    sum[0]+=int(data['data']['gntotal'])  #累计确诊
                    sum[1]+=int(data['data']['sustotal'])   
                    sum[2]+=int(data['data']['curetotal'])    # 累计治愈
                    sum[3]+=int(data['data']['deathtotal'])    # 累计死亡
                    sum[4]+=int(data['data']['add_daily']['addcon'])
                    sum[5]+=int(data['data']['add_daily']['addsus'])
                    sum[6]+=int(data['data']['add_daily']['addcure'])
                    sum[7]+=int(data['data']['add_daily']['adddeath'])
                    sum[8]+=int(data['data']['econNum'])  # 现存确诊
                    cdic['conNum'] = data['data']['gntotal']
                    cdic['susNum'] = data['data']['sustotal']
                    cdic['cureNum'] = data['data']['curetotal']
                    cdic['deathNum'] = data['data']['deathtotal']
                    cdic['conadd'] = data['data']['add_daily']['addcon']
                    cdic['susadd'] = data['data']['add_daily']['addsus']
                    cdic['cureadd'] = data['data']['add_daily']['addcure']
                    cdic['deathadd'] = data['data']['add_daily']['adddeath']
                    cdic['econNum'] = data['data']['econNum']
                else :
                    sum[0]+=int(dic[j]['conNum'])
                    sum[1]+=int(dic[j]['susNum'])
                    sum[2]+=int(dic[j]['cureNum'])
                    sum[3]+=int(dic[j]['deathNum'])
                    sum[4]+=int(dic[j]['conadd'])
                    sum[5]+=int(dic[j]['susadd'])
                    sum[6]+=int(dic[j]['cureadd'])
                    sum[7]+=int(dic[j]['deathadd']) 
                    sum[8]+=int(dic[j]['econNum'])
                    cdic['conNum'] = dic[j]['conNum']
                    cdic['susNum'] = dic[j]['susNum']
                    cdic['cureNum'] = dic[j]['cureNum']
                    cdic['deathNum'] = dic[j]['deathNum']
                    cdic['conadd'] = dic[j]['conadd']
                    cdic['susadd'] = dic[j]['susadd']
                    cdic['cureadd'] = dic[j]['cureadd']
                    cdic['deathadd'] = dic[j]['deathadd']    
                    cdic['econNum'] = dic[j]['econNum']
                cdic['name'] = name 
                ans[i]['country'].append(cdic)                           
        ans[i]['name'] = continent_list[i]
        ans[i]['conNum'] = sum[0]
        ans[i]['susNum'] = sum[1]
        ans[i]['cureNum'] = sum[2]
        ans[i]['deathNum'] = sum[3]
        ans[i]['conadd'] = sum[4]
        ans[i]['susadd'] = sum[5]
        ans[i]['cureadd'] = sum[6]      
        ans[i]['deathadd'] = sum[7]
        ans[i]['econNum'] = sum[8]
    with open('data/continent_list.json','w',encoding='utf-8') as f:
        json.dump(ans,f,ensure_ascii=False)
  
def scatter_diagram():
    days = [0,7,14,30]
    dic = [[] for i in range(4)]
    for i in range(len(country_code)): 
        citycode = country_code[i]
        filename = 'data/country/'+citycode+'.json'
        data = json.load(open(filename,encoding='utf-8'))
        coun = data['data']['country']
        data = data['data']['historylist']
        n = len(data)
        for k in range(4):
            j = days[k]
            dlis = []
            x = 100.0*float(data[j]['cureNum'])/float(data[j]['conNum'])
            dlis.append(format(x,'.2f'))
            x = 100.0*float(data[j]['deathNum'])/float(data[j]['conNum'])
            dlis.append(format(x,'.2f'))
            dlis.append(data[j]['conNum'])
            dlis.append(data[j]['cureNum'])
            dlis.append(data[j]['deathNum'])
            dlis.append(data[j]['conadd'])
            dlis.append(data[j]['cureadd'])
            dlis.append(data[j]['deathadd'])
            dlis.append(country_list[i])
            dic[k].append(dlis)
    with open('data/scatter_diagram.json','w',encoding='utf-8') as f:
        json.dump(dic,f,ensure_ascii=False)   
  
def news_and_rumors():
    '''
    url = 'https://lab.isaaclin.cn/nCoV/api/news?num=1000'
    filename = 'data/news.json'    
    get_data(url,filename)
    url = 'https://lab.isaaclin.cn/nCoV/api/rumors?num=1000&rumorType=0'
    filename = 'data/rumor0.json'    
    get_data(url,filename)
    url = 'https://lab.isaaclin.cn/nCoV/api/rumors?num=1000&rumorType=1'
    filename = 'data/rumor1.json'    
    get_data(url,filename)
    url = 'https://lab.isaaclin.cn/nCoV/api/rumors?num=1000&rumorType=2'
    filename = 'data/rumor2.json'    
    get_data(url,filename)
    '''
    r0 = json.load(open("data/rumor0.json",encoding='utf-8'))
    r1 = json.load(open("data/rumor1.json",encoding='utf-8'))
    r2 = json.load(open("data/rumor2.json",encoding='utf-8'))
    dic = {}
    dic['results'] = []
    for i in range(len(r0['results'])):
        x = r0['results'][i]
        x['type'] = 0
        dic['results'].append(x)
    for i in range(len(r1['results'])):
        x = r1['results'][i]
        x['type'] = 1
        dic['results'].append(x)
    for i in range(len(r2['results'])):
        x = r2['results'][i]
        x['type'] = 2
        dic['results'].append(x)
    random.shuffle(dic['results'])
    with open('data/rumor.json','w',encoding='utf-8') as f:
        json.dump(dic,f,ensure_ascii=False)   
    
    
def province_history():
    data = json.load(open("data/sina.json",encoding='utf-8'))
    data = data['data']['list']
    for i in range(len(data)):
        province = data[i]['ename']
        province_url = province
        if province=='xizang': province_url='tibet'
        if province=='neimenggu': province_url='inner mongolia'
        if province=='shanxis': province_url='shaanxi'
        if province=='xianggang': province_url='hong kong'
        if province=='aomen': province_url='macau'
        url = ''
        if province=='taiwan': url = 'https://corona.lmao.ninja/v2/historical/twn?lastdays=all'
        else : url = 'https://corona.lmao.ninja/v2/historical/chn/'+province_url+'?lastdays=all'
        filename = 'data/province/'+province+'.json' 
        get_data(url,filename)  
        now = json.load(open(filename,encoding='utf-8'))
        if 'message' in now.keys():
            print(url,' ', data[i]['name'])
        
if __name__ == '__main__': 

    print("start")
    starttime = datetime.datetime.now()
    
    #get_sina_api()  
    #continent()
    #scatter_diagram()
    news_and_rumors()
    #province_history()
    
    print("finish")
    endtime = datetime.datetime.now()
    print('total time: ',endtime-starttime)