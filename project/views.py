from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import numpy
import math
from .models import *
def distance(origin, destination):
 
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d


def index(request):
    if request.method == "POST":
        postalcode = request.POST["postalcode"]
        if not postalcode:
            return render(request, "project/index.html",{
                "message": "Enter a postal code.",
            })
        try:
            val = int(postalcode)
        except ValueError:
            return render(request, "project/index.html",{
                "message": "Please insert a number.",
            })
        try:
            post = Zipcode.objects.get(postal = postalcode)
        except Zipcode.DoesNotExist:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist in the database!",
            })
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
    #
        hawk = HawkerStall.objects.all()
        number = [0] * len(hawk)
        count = 0
        for haw in hawk.iterator():
            lat = haw.latitude
            long = haw.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        new_list = [x+1 for x in sort_index]
        number.sort()
        latitudes = [0] * len(hawk)
        longtitudes = [0] * len(hawk)
        names = [0] * len(hawk)
        addresses = [0] * len(hawk)
        recos = [0] * len(hawk)
        hours = [0] * len(hawk)
        details = [0] * len(hawk)
        contributors = [0] * len(hawk)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in new_list:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = HawkerStall.objects.get(id = i)
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(hawk)
        myhouselong = [longorigin] * len(hawk)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/index.html",{
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong
        })
    return render(request, "project/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "project/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "project/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "project/register.html")
