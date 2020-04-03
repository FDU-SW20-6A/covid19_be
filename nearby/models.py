from django.db import models
class city(models.Model):
    provinceName=models.CharField(max_length=30)
    provinceId=models.IntegerField()
    provinceTotal=models.IntegerField()
    cityName=models.CharField(max_length=30)
    cityId=models.IntegerField()
    cityLon=models.FloatField()
    cityLat=models.FloatField()
    cityLevel=models.IntegerField()
    cityCount=models.IntegerField()
    createdTime=models.DateTimeField(auto_now_add=True)
    changedTime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cityName

class pois(models.Model):
    poiName=models.CharField(max_length=30)
    lat=models.FloatField()
    lon=models.FloatField()
    tag=models.CharField(max_length=10)
    source=models.CharField(max_length=30)
    createdTime=models.DateTimeField(auto_now_add=True)
    changedTime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.poiName
