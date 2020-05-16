from django.test import TestCase
import requests,json

data={
    'username':'hsxia18',
    'password1':'123456',
    'password2':'123456',
    'authority':'user',
    'email':'18307130090@fudan.edu.cn',
}
raw='http://localhost:8001/'
url=raw+'user/register/'
resp=requests.post(url=url,json=data)
print(resp.text)
#cookies=resp.cookies

data={
    'userName':'hsxia18',
    'password':'123456',
}
url=raw+'user/login/'
resp=requests.post(url=url,json=data)
print(resp.text)
