import django
import csv,os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','covid19_be.settings')
django.setup()
from nearby.models import city,pois
with open(r'nearby\COVID-19-outbreak_area_data\data\City.csv','r',encoding='gbk',errors='ignore')as fp:
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

with open(r'nearby\COVID-19-outbreak_area_data\data\Pois.csv','r',encoding='gbk',errors='ignore')as fq:
    dictReaderx=csv.DictReader(fq)
    for rowx in dictReaderx:
        pois.objects.get_or_create(poiName=rowx['poiname'],lat=rowx['lat'],lon=rowx['lon'],tag=rowx['tag'],source=rowx['source'])

print('Done')