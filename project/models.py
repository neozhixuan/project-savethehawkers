from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class HawkerStall(models.Model):
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    address = models.CharField(blank = True, max_length = 200)
    hours = models.CharField(blank = True, null=True, max_length = 10)
    reco = models.CharField(blank = True, max_length = 100)
    details = models.CharField(blank = True, max_length = 1000)
    contributor = models.CharField(blank = True, max_length = 100)

    def __str__ (self):
        return f"{self.postal}, {self.building}"