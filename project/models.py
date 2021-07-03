from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Zipcode(models.Model):
    postal = models.IntegerField(null = True)
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    searchval = models.CharField(max_length = 200)
    blk_no = models.CharField(null=True, max_length = 10)
    road_name = models.CharField(max_length = 200)
    building = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)

    def __str__ (self):
        return f"{self.postal}, {self.building}"

class HawkerStall(models.Model):
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    name = models.CharField(blank = True, max_length = 200)
    stalltype = models.CharField(blank = True, max_length = 50)
    address = models.CharField(blank = True, max_length = 200)
    hours = models.CharField(blank = True, null=True, max_length = 300)
    reco = models.CharField(blank = True, max_length = 100)
    details = models.CharField(blank = True, max_length = 1000)
    contributor = models.CharField(blank = True, max_length = 100)
    image = models.ImageField(null = True, blank = True)

    def __str__ (self):
        return f"{self.address}, {self.name}, {self.reco}"

class History(models.Model):
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    name = models.CharField(blank = True, max_length = 200)
    stalltype = models.CharField(blank = True, max_length = 50)
    address = models.CharField(blank = True, max_length = 200)
    hours = models.CharField(blank = True, null=True, max_length = 300)
    reco = models.CharField(blank = True, max_length = 100)
    details = models.CharField(blank = True, max_length = 1000)
    contributor = models.CharField(blank = True, max_length = 100)

    def __str__ (self):
        return f"{self.address}, {self.name}, {self.reco}"