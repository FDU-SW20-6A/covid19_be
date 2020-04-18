# coding=utf-8
import re
import json

s = "西撒哈拉"
t = "非洲"
x = re.split(',|、|。| ',s)
#print(x)

dic = {}
dic = json.load(open('continent.json',encoding='utf-8'))

for i in range(len(x)):
    if x[i]!='':
        dic[str(x[i])]=t
        
with open('continent.json','w',encoding='utf-8') as f:
    json.dump(dic,f,ensure_ascii=False)

#print(dic)
