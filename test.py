import requests
import json

url='http://localhost:8002/user/test/'
data={
    'csrfmiddlewaretoken': ['RSPQFWn2T1Y9iCn62fRI2hRdt5P1XJMriuxGZey0riQbJ0JROTp01Nstc0i6Ylv2'],
    'username': ['xhs7700'],
    'password': ['(644000)xhs'],
    'captcha_0': ['d910c9f52e59a585a4271438320c40436e5a2f58'],
    'captcha_1': ['JRGN']
}

r=requests.post(url,json=data)
