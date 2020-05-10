from django.test import TestCase
import requests,json

data={
    'userName':'xhs7700',
    'password':'(644000)xhs'
}
raw='http://localhost:8001/'
url=raw+'user/login/'
headers={'Content-Type':'application/json'}
r=requests.post(url=url,headers=headers,data=json.dumps(data))
print(r.text)
x=r.cookies
print(r.cookies)

url=raw+'user/subscribe/add/'
data={
    'content':['110106','110107']
}
r=requests.post(url=url,cookies=x,headers=headers,data=json.dumps(data))
print(r.text)

url=raw+'user/logout/'
r=requests.get(url=url,cookies=x)
print(r.text)
