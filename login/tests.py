from django.test import TestCase
import requests,json

data={
    'username':'xhs7700',
    'isClear':'True',
    'content':['120000','510800'],
}
url='http://localhost:8001/user/subscribe/delete/'
headers={'Content-Type':'application/json'}
r=requests.post(url=url,headers=headers,data=json.dumps(data))
print(r.text)
