import requests,json
raw='http://localhost:8001/'
url=raw+'user/login/'
data={
    'userName':'xhs7700',
    'password':'(644000)xhs',
    'type':'account',
}
resp=requests.post(url,json=data)
c=resp.cookies
print(resp.text)
url=raw+'user/subscribe/post/'
data={
    'content':['310109','320200','230000']
}
resp=requests.post(url,json=data,cookies=c)
print(resp.text)
