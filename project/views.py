from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import numpy
import math

import telegram
from .models import *
from .models import User as UserProfile
from django import contrib, forms

from ipstack import GeoLookup
import requests
import json

from telegram import *
from django.conf import settings

import urllib

from datetime import date, datetime

from random import randrange

# NoReverseMatch: edity is not a name - probably didnt indicate app name in some html
# NoReverseMatch: argument (",") does not match.... - didnt include argument when your path requires one <str:...>
# NoReverseMatch: path does not exist - name you put is diff from "name" in urls
class CreateForm(forms.Form):
    postalcode = forms.IntegerField(label = "postalcode")
    image1 = forms.CharField(label = "image1", max_length = 200)
    name = forms.CharField(label = "name", max_length = 200)
    hours = forms.CharField(label = "hours", max_length = 300)
    reco = forms.CharField(label = "reco", max_length = 100)
    details = forms.CharField(label = "details", max_length = 1000)

class NewTaskForm (forms.Form):
    search = forms.CharField(label = "Food Recommendation:", min_length = 1, max_length = 50)
    postalcode = forms.IntegerField(label = "Postal Code:", min_value=1, max_value = 999999)

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
        history = History.objects.all()
        pagenumber = 1
        postalcode = request.POST["postalcode"]
        number = randrange(1,368)
        haw = HawkerStall.objects.filter(pk=number).first()
        # Error Tests
        if not postalcode:
            return render(request, "project/index.html",{
                "haw": haw,
                "message": "Enter a postal code.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history,
            })
        try:
            val = int(postalcode)
        except ValueError:
            return render(request, "project/index.html",{
                "haw": haw,
                "message": "Please insert a number.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "haw": haw,
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
            
        # Get values from API
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']

        # Calculate and sort distances to hawker stalls
        reco = request.POST['search']
        try:
            stalltypes = request.POST['stalltype']
            if not reco:
                hawk = HawkerStall.objects.filter(stalltype = stalltypes)
            else:
                hawk = HawkerStall.objects.filter(stalltype = stalltypes, reco__contains = reco)
        except KeyError:
            if not reco:
                hawk = HawkerStall.objects.all()
                stalltypes = 'Sup bitch'
            else:
                hawk = HawkerStall.objects.filter(reco__contains = reco)
                stalltypes = 'Sup bitch'
            
        


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
        #number = [1093,2765,4021...]
        #new_list = [104,210,57...]
        latitudes = [0] * len(hawk)
        longtitudes = [0] * len(hawk)
        names = [0] * len(hawk)
        addresses = [0] * len(hawk)
        recos = [0] * len(hawk)
        hours = [0] * len(hawk)
        details = [0] * len(hawk)
        contributors = [0] * len(hawk)
        # this will start from the numbers 4, then to 1, then to 6....
        if hawk == HawkerStall.objects.all():
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
        else:
            for i in sort_index:
                for j in range(len(addresses)):
                    if addresses[j] != 0:
                        j = j+1
                    else:
                        ha = hawk[int(i)]
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
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)


        return render(request, "project/index.html",{
            "latorigin": latorigin,
            "longorigin": longorigin,
            "reco": reco,
            "stalltype": stalltypes,
            "postalcode": postalcode,
            "pagenumber": pagenumber,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "namesjson": json.dumps(names),
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    
    comments = Comments.objects.all()
    history = History.objects.all()
    number = randrange(1,368)
    haw = HawkerStall.objects.filter(pk=number).first()
    hawk = HawkerStall.objects.all()
    numberoflistings = len(hawk)
    return render(request, "project/index.html",{
        "haw": haw,
        "no": "no",
        "form": NewTaskForm(),
        "history": history,
        "comments":comments,
        "numberoflistings": numberoflistings,
    })

def name(request):
    if request.method == "POST":
        name = request.POST['name']
        hawk = HawkerStall.objects.filter(name__contains = name)
        return render(request, "project/name.html", {
            "stalls": hawk,
        })

def nextindex(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        postalcode = request.POST["postalcode"]
            
        # Get values from API
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']

        stalltypes = request.POST['stalltype']
        reco = request.POST['reco']
        # Calculate and sort distances to hawker stalls
        if stalltypes == 'Sup bitch' and not reco:
            hawk = HawkerStall.objects.all()
        elif stalltypes == 'Sup bitch' and reco:
            hawk = HawkerStall.objects.filter(reco__contains = reco)
        elif reco:
            hawk = HawkerStall.objects.filter(stalltype = stalltypes, reco__contains = reco)
        else:
            hawk = HawkerStall.objects.filter(stalltype = stalltypes)
        
            
        

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
        #number = [1093,2765,4021...]
        #new_list = [104,210,57...]
        latitudes = [0] * len(hawk)
        longtitudes = [0] * len(hawk)
        names = [0] * len(hawk)
        addresses = [0] * len(hawk)
        recos = [0] * len(hawk)
        hours = [0] * len(hawk)
        details = [0] * len(hawk)
        contributors = [0] * len(hawk)
        # this will start from the numbers 4, then to 1, then to 6....
        if hawk == HawkerStall.objects.all():
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
        else:
            for i in sort_index:
                for j in range(len(addresses)):
                    if addresses[j] != 0:
                        j = j+1
                    else:
                        ha = hawk[int(i)]
                        latitudes[j] = ha.latitude
                        longtitudes[j] = ha.longtitude
                        names[j] = ha.name
                        addresses[j] = ha.address
                        recos[j] = ha.reco
                        hours[j] = ha.hours
                        details[j] = ha.details
                        contributors[j] = ha.contributor
                        break
        myhouselat = [latorigin] * (len(hawk) - (6*(page-1)))
        myhouselong = [longorigin] * (len(hawk) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/index.html",{
            "latorigin": latorigin,
            "longorigin": longorigin,
            "reco": reco,
            "number": stalltypes,
            "stalltype": stalltypes,
            "pagenumber": page,
            "postalcode": postalcode,
            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "namesjson": json.dumps(names[(6*(page-1)):]),
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })

def stalltype(request):
    if request.method == "POST":
        pagenumber = 1
        stalltypes = request.POST["stalltype"]
        postalcode = request.POST["postalcode"]
        history = History.objects.filter(id__in=[1,2,3,4,5,6])
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']
        results = HawkerStall.objects.filter(stalltype = stalltypes)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(results)
        myhouselong = [longorigin] * len(results)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/stall.html",{
            "pagenumber": pagenumber,
            "stalltypes": stalltypes,
            "postalcode": postalcode,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def nextstall(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        stalltypes = request.POST["stalltype"]
        postalcode = request.POST["postalcode"]
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
        results = HawkerStall.objects.filter(stalltype = stalltypes)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * (len(results) - (6*(page-1)))
        myhouselong = [longorigin] * (len(results) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/search.html",{
            "pagenumber": page,
            "stalltypes": stalltypes,
            "postalcode": postalcode,

            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })


def search(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            pagenumber = 1
            search = form.cleaned_data["search"]
            postalcode = form.cleaned_data["postalcode"]
            history = History.objects.filter(id__in=[1,2,3,4,5,6])
        try:
            address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address)
            data = response.text
            parse_json = json.loads(data)
            latorigin = float(parse_json['results'][0]['LATITUDE'])
        except IndexError:
            return render(request, "project/index.html",{
                "message": "Postal Code does not exist!",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
                "history": history
            })    
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        place = parse_json['results'][0]['ADDRESS']
        results = HawkerStall.objects.filter(reco__contains = search)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "No related results.",
                "form": NewTaskForm(),
                "postalcode": postalcode,
                "pagenumber": pagenumber,
                "no": "no",
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * len(results)
        myhouselong = [longorigin] * len(results)
        latandlong = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong2 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong3 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong4 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong5 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        latandlong6 = zip(myhouselat, myhouselong, latitudes, longtitudes)
        return render(request, "project/search.html",{
            "pagenumber": pagenumber,
            "search": search,
            "postalcode": postalcode,
            "latitudes": latitudes,
            "longtitudes": longtitudes,
            "names": names,
            "addresses": addresses,
            "recos": recos,
            "hours": hours,
            "details": details,
            "contributors": contributors,
            "numbers": number,
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def next(request, pagenumber):
    if request.method == "POST":
        page = int(pagenumber) + 1
        search = request.POST["search"]
        postalcode = request.POST["postalcode"]
        place = Zipcode.objects.filter(postal = postalcode)
        latorigin = place.first().latitude
        longorigin = place.first().longtitude
        results = HawkerStall.objects.filter(reco__contains = search)
        if not results:
            return render(request, "project/index.html", {
                "searchmessage": "That shit doesnt exist lmao",
                "form": NewTaskForm()
            })
        number = [0] * len(results)
        count = 0
        for res in results.iterator():
            lat = res.latitude
            long = res.longtitude
            origin = (latorigin, longorigin)
            destination = (lat, long)
            km = distance(origin, destination)
            km = km * 1000
            number[count] = round(km)
            count += 1
        #an array of the indexes after sorting
        s = numpy.array(number)
        sort_index = numpy.argsort(s)
        #original number = [2022, 3104, 1012...]
        #number = [1012, 2022, 3104...]
        #new_list = [3, 1, 2...]
        number.sort()
        latitudes = [0] * len(results)
        longtitudes = [0] * len(results)
        names = [0] * len(results)
        addresses = [0] * len(results)
        recos = [0] * len(results)
        hours = [0] * len(results)
        details = [0] * len(results)
        contributors = [0] * len(results)
        # this will start from the numbers 4, then to 1, then to 6....
        for i in sort_index:
            for j in range(len(addresses)):
                if addresses[j] != 0:
                    j = j+1
                else:
                    ha = results[int(i)]
                    latitudes[j] = ha.latitude
                    longtitudes[j] = ha.longtitude
                    names[j] = ha.name
                    addresses[j] = ha.address
                    recos[j] = ha.reco
                    hours[j] = ha.hours
                    details[j] = ha.details
                    contributors[j] = ha.contributor
                    break
        myhouselat = [latorigin] * (len(results) - (6*(page-1)))
        myhouselong = [longorigin] * (len(results) - (6*(page-1)))
        latandlong = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong2 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong3 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong4 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong5 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        latandlong6 = zip(myhouselat, myhouselong, latitudes[(6*(page-1)):], longtitudes[(6*(page-1)):])
        return render(request, "project/search.html",{
            "pagenumber": page,
            "search": search,
            "postalcode": postalcode,

            "latitudes": latitudes[(6*(page-1)):],
            "longtitudes": longtitudes[(6*(page-1)):],
            "names": names[(6*(page-1)):],
            "addresses": addresses[(6*(page-1)):],
            "recos": recos[(6*(page-1)):],
            "hours": hours[(6*(page-1)):],
            "details": details[(6*(page-1)):],
            "contributors": contributors[(6*(page-1)):],
            "numbers": number[(6*(page-1)):],
            "latandlong": latandlong,
            "latandlong2": latandlong2,
            "latandlong3": latandlong3,
            "latandlong4": latandlong4,
            "latandlong5": latandlong5,
            "latandlong6": latandlong6,
            "form": NewTaskForm()
        })
    return render(request, "project/index.html",{
        "form": NewTaskForm()
    })

def info(request, name):
    stall = HawkerStall.objects.filter(name = name).first()
    numberofcomments = len(stall.comments.all())
    orders = stall.comments.all().values('ordered')
    reco = stall.comments.all().values('recommend')
    items = [0] * len(orders)
    recommend = [0] * len(reco)
    for i in range(len(orders)):
        items[i] = orders[i]['ordered']
        recommend[i] = reco[i]['recommend']
    return render(request, "project/info.html",{
        "stalls": stall,
        "form": NewTaskForm(),
        "numberofcomments": numberofcomments,
        "comments": stall.comments.all(),
        "items": items,
        "recommend": recommend,
        "report": stall.report.all(),
        "count": stall.report.all().count(),
    })

def comment(request, name):
    if request.method == "POST":
        description = request.POST["description"]
        ordered = request.POST["ordered"]
        contributor = request.POST["contributor"]
        foodimage = request.FILES.get('foodimage')
        recommend = False
        if request.POST.get('recommend'):
            recommend = True
        else:
            recommend = False
        hawk = HawkerStall.objects.filter(name = name).first()
        f = Comments(comment = description, image = foodimage, ordered = ordered, stallname = name, address = hawk.address, contributor = contributor, recommend = recommend)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if result['success']:
            f.save()
            message = 'success'
            if request.user.is_authenticated:
                point = Point.objects.get(user = contributor)
                point.points = point.points + 5
                point.save()
        else:
            message = 'Invalid reCAPTCHA. Please try again.'
            return render(request, "project/info.html",{
                "stalls": hawk,
                "form": NewTaskForm(),
                "comments": hawk.comments.all(),
                "message": message
            })
        hawk.comments.add(f)
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'], text=f"Food Review! /n/n Description: {description}/n Stall:{name}/n Address: {hawk.address}", parse_mode=telegram.ParseMode.HTML)
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'], text=f"http://savethehawkers.herokuapp.com/images/{foodimage}")
        
        return render(request, "project/info.html",{
            "stalls": hawk,
            "form": NewTaskForm(),
            "comments": hawk.comments.all(),
            "message": message
        })
    hawk = HawkerStall.objects.filter(name = name).first()
    return render(request, "project/info.html",{
        "stalls": hawk,
        "form": NewTaskForm(),
        "comments": hawk.comments.all()
    })

def edity(request, name):
    if request.method == "POST":
        f = HawkerStall.objects.get(name = name)
        latitude = request.POST["latitude"]
        longtitude = request.POST["longtitude"]
        stalltype = request.POST["stalltype"]
        address = request.POST["address"]
        hours = request.POST["hours"]
        reco = request.POST["reco"]
        details = request.POST["details"]
        message = request.POST["message"]
        number = request.POST["number"]
        deals = request.POST["deals"]
        awards = request.POST["awards"]
        pricerange = request.POST["pricerange"]
        email = request.POST["email"]
        g = Email(email = email, datetime = datetime.now())
        g.save()
        if request.POST.get('fooddelivery'):
            f.fooddelivery = True
        else:
            f.fooddelivery = False
        if request.POST.get('phonedelivery'):
            f.phonedelivery = True
        else:
            f.phonedelivery = False
        if request.POST.get('freelance'):
            f.freelance = True
        else:
            f.freelance = False
        if request.POST.get('halal'):
            f.halal = True
        else:
            f.halal = False
        image = request.POST['image1']
        #contributor = request.POST["contributor"]
        f.image1 = image
        f.latitude = latitude
        f.longtitude = longtitude
        f.stalltype = stalltype
        f.address = address
        f.hours = hours
        f.reco = reco
        f.details = details
        f.message = message
        f.number = number
        f.deals = deals
        f.awards = awards
        f.pricerange = pricerange
        f.save()
        f.email.add(g)
        return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))
    else:
        return render(request, "project/index.html")

def report(request, name):
    if request.method == "POST":
        reason = request.POST['reason']
        user = request.POST['user']
        stallname = name
        f = Report(user = user, reason = reason, stallname = name)
        f.save()
        hawk = HawkerStall.objects.filter(name = name).first()
        hawk.report.add(f)
        return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))
    
def groupbuy(request):
    if request.method == "POST":
        destination = request.POST['postaldestination']
        areacollect = request.POST['area']
        contactinfo = request.POST['contact']
        additionalinfo = request.POST['text']
        postal = request.POST['postal']
        stallname = request.POST['stallname']
        address = f"https://developers.onemap.sg/commonapi/search?searchVal={postal}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(address)
        data = response.text
        parse_json = json.loads(data)
        latorigin = float(parse_json['results'][0]['LATITUDE'])
        longorigin = float(parse_json['results'][0]['LONGITUDE'])
        info = f"https://developers.onemap.sg/commonapi/search?searchVal={destination}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        response = requests.get(info)
        data = response.text
        parse_json = json.loads(data)
        lat2 = float(parse_json['results'][0]['LATITUDE'])
        long2 = float(parse_json['results'][0]['LONGITUDE'])
        blkno = parse_json['results'][0]['BLK_NO']
        address = parse_json['results'][0]['ROAD_NAME']
        website = "https://www.instagram.com/savethehawkers"
        f = Groupbuy(stallname = stallname, destination = destination, areacollect = areacollect, contactinfo = contactinfo, additionalinfo = additionalinfo, latorigin = latorigin, longorigin = longorigin, lat2=lat2, long2=long2)
        f.save()
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'], text=f"<b>A user has started a group buy!</b>\n\n<b>From:   </b><a href = 'http://savethehawkers.herokuapp.com/{stallname}/info'>{stallname}</a>\n<b>To:   </b><i>{blkno} {address}</i>\n<b>Details:   </b><i>{additionalinfo}</i> \n<b>Collect at:   </b><i>{areacollect}</i> \n<b>Contact Method:   </b> <i>{contactinfo}</i>\n\n<a href = 'https://www.instagram.com/savethehawkers'>savethehawkers</a>", parse_mode=telegram.ParseMode.HTML)
                
        return render(request, "project/groupbuy.html", {
            "groupbuys": Groupbuy.objects.all()
        })
    return render(request, "project/groupbuy.html", {
            "groupbuys": Groupbuy.objects.all()
        })


def userprofile(request, name):
    hawk = HawkerStall.objects.filter(contributor = name)
    report = Report.objects.filter(user = name)
    comments = Comments.objects.filter(contributor = name)
    points = Point.objects.get(user = name)
    user1 = UserProfile.objects.get(username = name)
    bookmarks = HawkerStall.objects.filter(bookmarks = user1)
    return render(request, "project/user.html",{
        "name": name,
        "hawker": hawk,
        "report": report,
        "comment": comments,
        "points" : points.points,
        "bookmarks": bookmarks,
    })

def bookmark(request, name):
    username = request.POST['username']
    user = UserProfile.objects.filter(username=username).first()
    hawk = HawkerStall.objects.get(name = name)
    hawk.bookmarks.add(user)
    return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))

def community(request):
    users = UserProfile.objects.all()
    return render(request, "project/community.html", {
        "users" : users,
    })

# def delete(request, name):
    # g = HawkerStall.objects.filter(name = name).first()
    # g.latitude = 0
    # g.longtitude = 0
    # g.stalltype = ""
    # g.address = ""
    # g.hours = ""
    # g.reco = ""
    # g.details = ""
    # g.name = ""
    # g.contributor = ""
    # g.save()
    # return HttpResponseRedirect(reverse("savethehawkers:index"))

def creations(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            image1 = form.cleaned_data["image1"] 
            postalcode = form.cleaned_data["postalcode"] 
            name = form.cleaned_data["name"]
            hours = form.cleaned_data["hours"]
            reco = form.cleaned_data["reco"]
            details = form.cleaned_data["details"]
            contributor = request.POST["contributor"]
            stalltype = request.POST["stalltype"]
            number = request.POST["number"]
            if request.POST.get('halal'):
                halal = True
            else:
                halal = False
            try:
                address2 = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
                response = requests.get(address2)
                data = response.text
                parse_json = json.loads(data)
                latitude = float(parse_json['results'][0]['LATITUDE'])
            except IndexError:
                message = "Form invalid"
                return render(request, "project/create.html", {
                "form3": CreateForm(),
                "message": message,
                })   
            
            # Get values from API
            address2 = f"https://developers.onemap.sg/commonapi/search?searchVal={postalcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
            response = requests.get(address2)
            data = response.text
            parse_json = json.loads(data)
            latitude = float(parse_json['results'][0]['LATITUDE'])
            longtitude = float(parse_json['results'][0]['LONGITUDE'])
            address3 = parse_json['results'][0]['ADDRESS']

            h = HawkerStall(postalcode= postalcode, latitude= latitude, longtitude= longtitude, name= name, stalltype = stalltype, address = address3, hours = hours, reco = reco, details = details, contributor = contributor, image1 = image1)
            i = History(halal = halal, number = number, latitude= latitude, longtitude= longtitude, name= name, stalltype = stalltype, address = address3, hours = hours, reco = reco, details = details, contributor = contributor)
            h.save()
            i.save()
            return HttpResponseRedirect(reverse("savethehawkers:info", args=(name,)))
        else:
            message = "Form invalid"
            return render(request, "project/create.html", {
            "form3": CreateForm(),
            "message": message,
            })
    else:
        return render(request, "project/create.html",{
            "form3": CreateForm(),
            })

###########################
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("savethehawkers:users", args=(username,)))
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("savethehawkers:index"))


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
            user = UserProfile.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "project/register.html", {
                "message": "Username already taken."
            })
        f = Point(user = username, points = 0)
        f.save()
        login(request, user)
        return HttpResponseRedirect(reverse("savethehawkers:index"))
    else:
        return render(request, "project/register.html")
