import requests,json
raw='http://localhost:8001/'
url=raw+'nearby/'
data={
    'lon':120,
    'lat':'30',
    'citycode':'310110'
}
resp=requests.get(url,data)
print(resp.text)
