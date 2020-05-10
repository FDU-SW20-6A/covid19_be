import json
from xpinyin import Pinyin
localdata=json.load(open(r'./data/news.json','r',encoding='utf-8',errors='ignore'))['results']
sinadata=json.load(open(r'./data/sina.json','r',encoding='utf-8',errors='ignore'))['data']['list']
keys=[]
citys={}
provcode={'香港':'81','澳门':'82','台湾':'71'}
for province in sinadata:
    provname=province['name']
    keys.append(province['name'])
    citys[provname]=[provname]
    for city in province['city']:
        if(city['name'] in{'境外输入人员','外地来京人员','外地来沪人员','境外输入','外地来津','外省输入'}):continue
        x=city['name']
        if len(x)>3 and x[-3:] in {'自治州','示范区'}:
            x=x[:-3]
        elif len(x)>3 and x[-2:]in{'林区','地区','新区'}:
            x=x[:-2]
        elif len(x)>2 and x[-1:] in {'市','区','州'}:
            x=x[:-1]
        if city['citycode']!='':
            if not provname in provcode:
                provcode[provname]=city['citycode'][2:4]
        keys.append(x)
        citys[provname].append(x)

newslist=[]
for news in localdata:
    summary=news['summary']
    flag=0
    for prov in citys.keys():
        for city in citys[prov]:
            if summary.find(city)!=-1:
                if city=='北京' and summary.find('北京时间')!=-1:continue
                #print(news)
                news['province']=prov
                news['provinceId']=provcode[prov]
                newslist.append(news)
                flag=1
                break
        if flag==1:
            break
provdata={}
for x in provcode.values():provdata[x]=[]
for news in newslist:
    id=news['provinceId']
    news.pop('province')
    news.pop('provinceId')
    provdata[id].append(news)
json.dump(provdata,open(r'./data/localnews.json','w',encoding='utf-8'))
'''
s=bytes(json.dumps(provdata),encoding='utf-8').decode('unicode_escape')
print(s)
'''
f=open(r'./data/localnews.json','r',encoding='unicode_escape')
ab
