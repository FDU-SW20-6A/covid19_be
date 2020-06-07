from django.test import TestCase,Client
from .models import city,pois
from .views import dictError
import unittest,json,csv

def dictErrorBytes(lon,lat):
    data=bytes(json.dumps(dictError(lon,lat)),encoding='utf-8')
    return data

def nearbyInitInput(markersNum):
    return {'markersNum':markersNum}

def nearbyInitGet(self,data):
    resp=self.client.get('/nearby/init/',data)
    respdata=json.loads(resp.content)
    return resp,respdata

def nearbyInput(lon,lat,citycode,num):
    return {'lon':lon,'lat':lat,'citycode':citycode,'markersNum':num}

def nearbyGet(self,data):
    resp=self.client.get('/nearby/',data)
    respdata=json.loads(resp.content)
    return resp,respdata

def lonlatDict(lon,lat):
    return {"longitude": lon, "latitude": lat}

def insertData():
    fp=open(r'nearby\COVID-19-outbreak_area_data\data\City.csv','r',encoding='gbk',errors='ignore')
    fq=open(r'nearby\COVID-19-outbreak_area_data\data\Pois.csv','r',encoding='gbk',errors='ignore')
    dictReader=csv.DictReader(fp)
    for row in dictReader:
        city.objects.get_or_create(
            provinceName=row['provinceName'],
            provinceId=row['provinceId'],
            provinceTotal=row['provinceTotal'],
            cityName=row['cityName'],
            cityId=row['cityId'],
            cityLon=row['cityLon'],
            cityLat=row['cityLat'],
            cityLevel=row['cityLevel'],
            cityCount=row['cityCount']
        )
    fp.close()
    dictReaderx=csv.DictReader(fq)
    for rowx in dictReaderx:
        pois.objects.get_or_create(poiName=rowx['poiname'],lat=rowx['lat'],lon=rowx['lon'],tag=rowx['tag'],source=rowx['source'])
    fq.close()

def nearbyInitTestNormal(self):
    lon,lat,num=121.505236,31.300102,5
    data=nearbyInitInput(num)
    resp,respdata=nearbyInitGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(respdata['mapCenter'],lonlatDict(lon,lat))
    self.assertEqual(len(respdata['markers']),num)

def nearbyInitTestDefault(self):
    lon,lat=121.505236,31.300102
    data={}
    resp,respdata=nearbyInitGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(respdata['mapCenter'],lonlatDict(lon,lat))
    self.assertEqual(len(respdata['markers']),10)

def nearbyInitTestFloatMarkersNum(self):
    lon,lat,num=121.505236,31.300102,5.5
    data=nearbyInitInput(num)
    resp,respdata=nearbyInitGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(resp.content,dictErrorBytes(lon,lat))

def nearbyInitTestStrMarkersNum(self):
    lon,lat,num=121.505236,31.300102,'5'
    data=nearbyInitInput(num)
    resp,respdata=nearbyInitGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(respdata['mapCenter'],lonlatDict(lon,lat))
    self.assertEqual(len(respdata['markers']),eval(num))

def nearbyInitTestNegativeMarkersNum(self):
    lon,lat,num=121.505236,31.300102,-2
    data=nearbyInitInput(num)
    resp,respdata=nearbyInitGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(resp.content,dictErrorBytes(lon,lat))

def nearbyTestNormal(self):
    lon,lat=121.463278,31.194057
    data=nearbyInput(lon,lat,'310104',20)
    resp,respdata=nearbyGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(respdata['mapCenter'],lonlatDict(lon,lat))

def nearbyTestFloatMarkersNum(self):
    lon,lat,citycode,num=120,30,'310110',5.5
    data=nearbyInput(lon,lat,citycode,num)
    resp,respdata=nearbyGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(resp.content,dictErrorBytes(lon,lat))

def nearbyTestNegativeMarkersNum(self):
    lon,lat,citycode,num=120,30,'310110',-3
    data=nearbyInput(lon,lat,citycode,num)
    resp,respdata=nearbyGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(resp.content,dictErrorBytes(lon,lat))

def nearbyTestWrongLonLat(self):
    lonList=[50,-5.5,150,6.0]
    latList=[2,-3.0,70,89.0]
    lon,lat,citycode,num=120,30,'310110',5
    for Lon in lonList:
        data=nearbyInput(Lon,lat,citycode,num)
        resp,respdata=nearbyGet(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictErrorBytes(Lon,lat))
    for Lat in latList:
        #print('Lat:',Lat)
        data=nearbyInput(lon,Lat,citycode,num)
        resp,respdata=nearbyGet(self,data)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,dictErrorBytes(lon,Lat))

def nearbyTestInvalidCitycode(self):
    lon,lat,citycode,num=120,30,'31011',5
    data=nearbyInput(lon,lat,citycode,num)
    resp,respdata=nearbyGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(resp.content,dictErrorBytes(lon,lat))

def nearbyTestWrongCitycode(self):
    lon,lat,citycode,num=120,30,'abcdef',5
    data=nearbyInput(lon,lat,citycode,num)
    resp,respdata=nearbyGet(self,data)
    self.assertEqual(resp.status_code,200)
    self.assertEqual(respdata['mapCenter'],lonlatDict(lon,lat))
    self.assertEqual(len(respdata['markers']),num)
    self.assertEqual(respdata['city'],'unknown')

class NearbyInitTest(TestCase):
    def setUp(self):
        insertData()
        self.client=Client()

    def testAll(self):
        nearbyInitTestNormal(self)
        nearbyInitTestDefault(self)
        nearbyInitTestStrMarkersNum(self)
        nearbyInitTestFloatMarkersNum(self)
        nearbyInitTestNegativeMarkersNum(self)

class NearbyTest(TestCase):
    def setUp(self):
        insertData()
        self.client=Client()

    def testAll(self):
        nearbyTestNormal(self)
        nearbyTestFloatMarkersNum(self)
        nearbyTestNegativeMarkersNum(self)
        nearbyTestWrongLonLat(self)
        nearbyTestInvalidCitycode(self)
        nearbyTestWrongCitycode(self)
