# coding=utf-8
import requests
import json
import datetime
import time

def get_data(url,filename):

    with requests.get(url) as r:
        if r.status_code == 200:
            data = r.json()  
            try :
                with open(filename,'w',encoding='utf-8') as f:
                    json.dump(data,f,ensure_ascii=False)
            except :
                with open(filename,'w',encoding='utf-8') as f:
                    f.write(str(data))
        else:
            print(url,' fail') 
    return
    
    
def get_sina_api():

    url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json'
    filename = 'data/sina.json'    
    get_data(url,filename)

    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['otherlist']
    lis = []
    
    for i in range(len(dic)): 
        name = dic[i]['name']
        citycode = dic[i]['citycode']
        url = 'https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode='+citycode
        filename = 'data/country/'+citycode+'.json'
        if citycode!='': get_data(url,filename)

def continent():

    continent_list = ['亚洲','欧洲','非洲','大洋洲','北美洲','南美洲','其它']
    con = json.load(open('data/continent.json',encoding='utf-8'))
    data = json.load(open("data/sina.json",encoding='utf-8'))
    dic = data['data']['worldlist']
    ans = [{} for i in range(7)]
    for i in range(len(continent_list)):
        sum = [0 for j in range(8)]
        ans[i]['country'] = []
        for j in range(len(dic)): 
            name = dic[j]['name']
            #If a new country appears, but we don't know which continent it belongs to, ignore it
            if name in con and con[name]==continent_list[i]:
                cdic = {}
                if name=='中国':
                    sum[0]+=int(data['data']['gntotal'])
                    sum[1]+=int(data['data']['sustotal'])
                    sum[2]+=int(data['data']['curetotal'])
                    sum[3]+=int(data['data']['deathtotal'])
                    sum[4]+=int(data['data']['add_daily']['addcon'])
                    sum[5]+=int(data['data']['add_daily']['addsus'])
                    sum[6]+=int(data['data']['add_daily']['addcure'])
                    sum[7]+=int(data['data']['add_daily']['adddeath'])
                    cdic['conNum'] = data['data']['gntotal']
                    cdic['susNum'] = data['data']['sustotal']
                    cdic['cureNum'] = data['data']['curetotal']
                    cdic['deathNum'] = data['data']['deathtotal']
                    cdic['conadd'] = data['data']['add_daily']['addcon']
                    cdic['susadd'] = data['data']['add_daily']['addsus']
                    cdic['cureadd'] = data['data']['add_daily']['addcure']
                    cdic['deathadd'] = data['data']['add_daily']['adddeath']
                else :
                    sum[0]+=int(dic[j]['conNum'])
                    sum[1]+=int(dic[j]['susNum'])
                    sum[2]+=int(dic[j]['cureNum'])
                    sum[3]+=int(dic[j]['deathNum'])
                    sum[4]+=int(dic[j]['conadd'])
                    sum[5]+=int(dic[j]['susadd'])
                    sum[6]+=int(dic[j]['cureadd'])
                    sum[7]+=int(dic[j]['deathadd']) 
                    cdic['conNum'] = dic[j]['conNum']
                    cdic['susNum'] = dic[j]['susNum']
                    cdic['cureNum'] = dic[j]['cureNum']
                    cdic['deathNum'] = dic[j]['deathNum']
                    cdic['conadd'] = dic[j]['conadd']
                    cdic['susadd'] = dic[j]['susadd']
                    cdic['cureadd'] = dic[j]['cureadd']
                    cdic['deathadd'] = dic[j]['deathadd']    
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
    with open('data/continent_list.json','w',encoding='utf-8') as f:
        json.dump(ans,f,ensure_ascii=False)
        
    
if __name__ == '__main__': 

    print("start")
    starttime = datetime.datetime.now()
    
    get_sina_api()  
    continent()
    
    print("finish")
    endtime = datetime.datetime.now()
    print('total time: ',endtime-starttime)