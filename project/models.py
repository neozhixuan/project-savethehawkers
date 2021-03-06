from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Zipcode(models.Model):
    postal = models.IntegerField(null = True, max_length = 255)
    latitude = models.FloatField(null = True, max_length = 255)
    longtitude = models.FloatField(null = True, max_length = 255)
    searchval = models.CharField(max_length = 200)
    blk_no = models.CharField(null=True, max_length = 255)
    road_name = models.CharField(max_length = 200)
    building = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)

    def __str__ (self):
        return f"{self.postal}, {self.building}"
class Comments(models.Model):
    comment = models.CharField(blank = True, max_length = 500)
    image = models.ImageField(null = True, blank = True)
    ordered = models.CharField(blank = True, null=True, max_length = 1000)
    stallname = models.CharField(blank = True, null=True, max_length = 1000)
    recommend = models.BooleanField(blank = True, null = True)
    address = models.CharField(blank = True, null=True, max_length = 1000)
    contributor = models.CharField(blank = True, null = True,  max_length = 1000)
    def __str__ (self):
        return f"{self.comment}"

class Menu(models.Model):
    image = models.ImageField(null = True, blank = True)

class Report(models.Model):
    user = models.CharField(blank = True, null=True, max_length = 1000)
    reason = models.CharField(blank = True, null=True, max_length = 1000)
    stallname = models.CharField(blank = True, null=True, max_length = 1000)
    def __str__ (self):
        return f"{self.reason}"

class Email (models.Model):
    email = models.CharField(blank = True, max_length = 1000)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    def __str__ (self):
        return f"{self.email}, {self.datetime}"

class District (models.Model):
    email = models.CharField(blank = True, max_length = 1000)
    def __str__ (self):
        return f"{self.email}"

class HawkerStall(models.Model):
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    name = models.CharField(blank = True, null = True,  max_length = 200)
    stalltype = models.CharField(blank = True, null = True,  max_length = 255)
    postalcode = models.IntegerField(blank = True, null = True, max_length = 255)
    address = models.CharField(blank = True, null = True,  max_length = 200)
    hours = models.CharField(blank = True, null=True, max_length = 300)
    reco = models.TextField(blank = True, null = True, max_length = 1000)
    details = models.CharField(blank = True, null = True,  max_length = 10000)
    contributor = models.CharField(blank = True, null = True,  max_length = 1000)
    image1 = models.CharField(blank = True, null = True,  max_length = 2000)
    image2 = models.CharField(blank = True, null = True,  max_length = 2000)
    image3 = models.CharField(blank = True, null = True,  max_length = 2000)
    image4 = models.CharField(blank = True, null = True,  max_length = 2000)
    image5 = models.CharField(blank = True, null = True,  max_length = 2000)
    comments = models.ManyToManyField(Comments, blank = True, null = True)
    message = models.CharField(blank = True, null=True, max_length = 300)
    number = models.IntegerField(blank = True, null = True, max_length = 255)
    fooddelivery = models.BooleanField(blank = True, null = True)
    phonedelivery = models.BooleanField(blank = True, null = True)
    freelance = models.BooleanField(blank = True, null = True)
    halal = models.BooleanField(blank = True, null = True)
    deals = models.CharField(blank = True, null=True, max_length = 1000)
    menu = models.ManyToManyField(Menu, blank = True, null = True)
    awards = models.CharField(blank = True, null=True, max_length = 500)
    pricerange = models.CharField(blank = True, null=True, max_length = 1000)
    facebook = models.CharField(blank = True, null=True, max_length = 1000)
    twitter = models.CharField(blank = True, null=True, max_length = 1000)
    report = models.ManyToManyField(Report, blank = True, null = True)
    email = models.ManyToManyField(Email, blank = True, null = True )
    bookmarks = models.ManyToManyField(User, blank = True, null = True )
    district = models.ForeignKey(District, blank = True, null = True, on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.address}, {self.name}, {self.reco}"


class History(models.Model):
    latitude = models.FloatField(null = True, max_length = 255)
    longtitude = models.FloatField(null = True, max_length = 255)
    name = models.CharField(blank = True, max_length = 200)
    stalltype = models.CharField(blank = True, max_length = 255)
    address = models.CharField(blank = True, max_length = 200)
    hours = models.CharField(blank = True, null=True, max_length = 300)
    reco = models.CharField(blank = True, max_length = 1000)
    details = models.CharField(blank = True, max_length = 10000)
    contributor = models.CharField(blank = True, max_length = 1000)

    def __str__ (self):
        return f"{self.address}, {self.name}, {self.reco}"

class Point(models.Model):
    user = models.CharField(blank = True, null=True, max_length = 1000)
    points = models.IntegerField(blank = True, null = True, max_length = 255)
    def __str__ (self):
        return f"{self.user}: {self.points} points"

class Groupbuy(models.Model):
    stallname = areacollect = models.CharField(blank = True, null=True, max_length = 100)
    destination = models.IntegerField(blank = True, null = True, max_length = 255)
    areacollect = models.CharField(blank = True, null=True, max_length = 1000)
    contactinfo = models.CharField(blank = True, null=True, max_length = 1000)
    additionalinfo = models.CharField(blank = True, null=True, max_length = 10000)
    latorigin = models.FloatField(null = True, blank = True, max_length = 255)
    longorigin = models.FloatField(null = True, blank = True, max_length = 255)
    lat2 = models.FloatField(null = True, blank = True, max_length = 255)
    long2 = models.FloatField(null = True, blank = True, max_length = 255)

    def __str__ (self):
        return f"{self.additionalinfo}"