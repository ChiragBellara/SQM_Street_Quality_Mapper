'''Importing necessary modules from python and django library'''

from django.shortcuts import render
from django.conf import settings
from pothole import views
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.views.generic import View
from django.http import HttpResponse
from statistics import mean
import csv
import json
from array import *
import re
import os
import numpy as np
import math
from firebase import firebase
import pylab
import pandas as pd
from datetime import datetime
from datetime import timedelta
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

"""/* A function to store x,y,z values from the csv generated /*"""


def xyzValues():
    with open(os.path.join(settings.MEDIA_ROOT, "data1_0.csv"), 'r') as k:
        data = [d for d in list(csv.reader(k, delimiter=',')) if d != []]
        print(data[0][0])
        t = [str(data[i][0]) for i in range(len(data)) if data[i][0] != '']
        x = [float(data[i][1]) for i in range(len(data)) if data[i][1] != '']
        y = [float(data[i][2]) for i in range(len(data)) if data[i][2] != '']
        z = [float(data[i][3]) for i in range(len(data)) if data[i][3] != '']

        return [t, x, y, z]


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        t, x, y, z = xyzValues()
        return t

    def get_providers(self):
        return ["x-axis", "y-axis", "z-axis"]

    def get_data(self):
        t, x, y, z = xyzValues()
        return [x, y, z]


class LineChartJSONViewRide(BaseLineChartView):
    def get_labels(self):
        t, x, y, z = xyzValues()
        return t

    def get_providers(self):
        return ["Ride-Quality_Score"]

    def get_data(self):
        t, x, y, z = xyzValues()
        score = []
        for i in range(len(x)):
            score.append(math.sqrt((x[i]**2 + y[i]**2 + z[i]**2)))
        # score = math.sqrt((x**2 + y**2 + z**2))
        # score = float(score)
        return [score]


class RadarChartJSONViewRide(BaseLineChartView):
    def get_labels(self):
        return ["High", "Medium", "Low"]

    def get_providers(self):
        return ["High Intensity", "Medium Intensity", "Low Intensity"]

    def get_data(self):
        hc, mc, lc = [], [], []
        for i in range(0, 100, 10):
            hc.append(i)
        for j in range(0, 70, 10):
            mc.append(j)
        for k in range(0, 82, 10):
            lc.append(i)
        # score = float(score)
        return [[76, 0, 0], [0, 82, 0], [0, 0, 63]]


line_chart = TemplateView.as_view(template_name='pothole/analytics.html')
line_chart_json = LineChartJSONView.as_view()

line_chart_json_ride = LineChartJSONViewRide.as_view()

radar_chart_json = RadarChartJSONViewRide.as_view()


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return redirect('/dashboard')
            else:
                return render(request, 'pothole/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'pothole/index.html', {'error_message': 'Invalid login'})
    return render(request, 'pothole/index.html')


def logout_user(request):
    logout(request)
    return render(request, 'pothole/index.html')

# Create your views here.


def index(request):
    return render(request, 'pothole/index.html')

# Routes
# 1. Not logged in:
    # check if logged in: /check
    # if authenticated go to /dashboard
    # else /loginpage


def check(request):
    print("I m chcek")
    if request.session.has_key('username'):
        print("I m authenticated")
        return render(request, 'pothole/dashboard.html')
    else:
        return render(request, 'pothole/login.html')


def login(request):
    return render(request, 'pothole/dashboard.html')


def logout(request):
    return render(request, 'pothole/index.html')


def dashboard(request):
    return render(request, 'pothole/dashboard.html')


def analytics(request):
    return render(request, 'pothole/analytics.html')


def pothole(request):
    final_data = []
    count = 0
    data_Arr = []
    avg_pothole = []
    time_str1 = "00:00:20"
    time_str2 = "00:00:00"
    format = "%H:%M:%S"
    timestamp_1 = datetime.strptime(time_str1, format)
    timestamp_2 = datetime.strptime(time_str2, format)
    timestamp_init = timestamp_1 - timestamp_2
    print(timestamp_init)

    with open('{}/'.format(settings.MEDIA_ROOT)+"feeds.csv", 'r') as log:
        total = 0
        output = []
        read_logs = csv.DictReader(log, delimiter=',', quotechar='|')
        i = 1
        j = 0
        k = 0
        for row in read_logs:
            if row['field3'] == 'z':
                continue
            total += float(row['field3'])
            timestamp = str(row['created_at'])
            acc = float(row['field3'])
            latitude = str(row['field4'])
            longitude = str(row['field5'])
            ridescore = str(row['field6'])
            output.append(float(row['field3']))
            data_Arr.insert(
                i, [timestamp, acc, latitude, longitude, ridescore])
            count += 1
            i += 1
        avg = total/count
        # print(data_Arr)
        for item in data_Arr:
            timestamp = item[0]
            new_tstmp = timestamp.split('_')
            # timestamp = new_tstmp[1].strip(':')
            item[0] = new_tstmp[0][:4] + "-" + new_tstmp[0][4:6] + "-" + new_tstmp[0][6:8] + \
                " " + new_tstmp[1][:2] + ":" + \
                new_tstmp[1][2:4] + ":" + new_tstmp[1][4:6]
            # print(item[0])
            acc_z = item[1]
            diff = avg - float(acc_z)
            diff = abs(diff)
            if diff > 2:
                if j == 0:
                    avg_pothole.insert(j, [item[0], diff])
                    # print(str(timestamp)+' , '+str(diff)+" :Pothole Detected")
                    final_ts = item[0]
                else:
                    fmt = '%Y-%m-%d %H:%M:%S'
                    tstamp1 = datetime.strptime(item[0], fmt)
                    tstamp2 = datetime.strptime(data_Arr[j-1][0], fmt)
                    # print("Time 1: "+str(tstamp1))
                    # print("Time 2: "+str(tstamp2))
                    difference_tstmp = tstamp1 - tstamp2
                    # print(difference_tstmp)

                    if difference_tstmp > timestamp_init:
                        avg_pothole.insert(j, [timestamp, diff])
                    final_ts = item[0]

                if diff >= 2 and diff <= 4:
                    # print("Medium")
                    intensity = "Medium"
                else:
                    # print("High")
                    intensity = "High"
                final_data.insert(
                    k, [final_ts, item[2], item[3], item[4], intensity])
                k = k+1
            j += 1
        print(final_data)
        return render(request, 'pothole/pothole.html', {'final_data': final_data})


def sessionfn(request):
    return HttpResponse(request.session)
    # print(request.session)


def getcolorcode(score):
    if score >= 8.381720005464272 and score <= 8.63253751062201:
        color = '#003300'
    elif score > 8.63253751062201 and score <= 8.883355015779747:
        color = '#009900'
    elif score > 8.883355015779747 and score <= 9.134172520937485:
        color = '#00CC33'
    elif score > 9.134172520937485 and score <= 9.384990026095222:
        color = '#CC9900'
    elif score > 9.384990026095222 and score <= 9.63580753125296:
        color = '#CCCC00'
    elif score > 9.63580753125296 and score <= 9.886625036410697:
        color = '#CCFF00'
    elif score > 9.886625036410697 and score <= 10.137442541568435:
        color = '#880000'
    elif score > 10.137442541568435 and score <= 10.388260046726172:
        color = '#580000'
    else:
        color = '#380000'
    return color


def map(request):
    # retrievefirebase()
    data = PolylineData.objects.all()

    os.chdir(settings.MEDIA_ROOT)
    locations = []
    for f in data:
        with open('{}/'.format(settings.MEDIA_ROOT) + f.filename) as k:
            all_data = list(csv.reader(k, delimiter=','))

        i = 0
        for m in range(0, len(all_data), 20):
            with open('{}/'.format(settings.MEDIA_ROOT) + f.filename.rstrip('.csv') + '_{}.csv'.format(i), 'w+') as t:
                w = csv.writer(t, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
                for row in all_data[m:m+21]:
                    w.writerow(row)
                i += 1

    f = [f for f in os.listdir(settings.MEDIA_ROOT)
         if re.search(r'.*_.*\.csv$', f)]

    for everyfile in f:
        with open(everyfile, 'r') as k:
            lis = []
            locationcol = {}
            data = [d for d in list(csv.reader(k, delimiter=',')) if d != []]
            # print(data)
            x = mean([float(data[i][1])
                     for i in range(len(data)) if data[i][1] != ''])
            y = mean([float(data[i][2])
                     for i in range(len(data)) if data[i][2] != ''])
            z = mean([float(data[i][3])
                     for i in range(len(data)) if data[i][3] != ''])
            score = math.sqrt((x**2 + y**2 + z**2))

            latitude = [float(data[i][4])
                        for i in range(len(data)) if data[i][4] != '']
            # print(len(latitude))
            longitude = [float(data[i][5])
                         for i in range(len(data)) if data[i][5] != '']
            # print(len(longitude))
            for lat, longi in zip(latitude, longitude):
                lis.append({"lat": lat, "lng": longi})

            locationcol['location'] = lis
            locationcol['color'] = getcolorcode(score)
            locations.append(locationcol)
            # print(locations)

    context = {
        'locations': locations
    }
    return render(request, 'pothole/map.html', context)


def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y) - 1):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter[i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])

    print(np.asarray(signals))
    return dict(signals=np.asarray(signals),
                avgFilter=np.asarray(avgFilter),
                stdFilter=np.asarray(stdFilter))


def locations(request):
    locations = []
    os.chdir(settings.MEDIA_ROOT)
    f = [f for f in os.listdir(settings.MEDIA_ROOT)
         if re.search(r'.*_.*\.csv$', f)]

    for everyfile in f[:5]:
        with open(everyfile, 'r') as k:
            data = [d for d in list(csv.reader(k, delimiter=',')) if d != []]
            lis = []
            locationcol = {}
            lati_l = []
            longi_l = []
            print(data)
            # Data
            y = np.array([float(data[i][3])
                         for i in range(len(data)) if data[i][3] != ''])
            lat = np.array([float(data[i][4])
                           for i in range(len(data)) if data[i][4] != ''])
            lon = np.array([float(data[i][5])
                           for i in range(len(data)) if data[i][5] != ''])
            # Settings: lag = 30, threshold = 5, influence = 0
            lag = 4
            threshold = 3
            influence = 0.5

            # Run algo with settings from above
            result = thresholding_algo(
                y, lag=lag, threshold=threshold, influence=influence)
            # print(result)

            # Plot result
            # pylab.subplot(211)
            # pylab.plot(np.arange(1, len(y)+1), y)

            # pylab.plot(np.arange(1, len(y)+1),
            #            result["avgFilter"], color="cyan", lw=2)

            # pylab.plot(np.arange(1, len(y)+1),
            #            result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)

            # pylab.plot(np.arange(1, len(y)+1),
            #            result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)

            # pylab.subplot(212)
            # pylab.step(np.arange(1, len(y)+1), result["signals"], color="red", lw=2)
            # pylab.ylim(-1.5, 1.5)
            # pylab.show()

            for i in range(0, len(result["signals"])):
                if (result["signals"][i] == 1 or result["signals"][i] == -1):
                    lati_l.insert(i, lat[i])
                    longi_l.insert(i, lon[i])

            print("latitude list", lati_l)
            print("longitude list", longi_l)
            for lat, longi in zip(lati_l, longi_l):
                lis.append({"lat": lat, "lng": longi})

            locationcol['location'] = lis
            locations.append(locationcol)

    context = {
        'locations': locations
    }
    return render(request, 'pothole/locations.html', context)


def retrievefirebase():
    fire = firebase.FirebaseApplication(
        'https://squid-3349a.firebaseio.com/', None)

    lat = list(fire.get('/GPS/Lat', None).values())[:21]
    lon = list(fire.get('/GPS/Long', None).values())[:21]
    timestampG = list(fire.get('/GPS/Timestamp', None).values())[:21]

    x1 = list(fire.get('/A1/Ax', None).values())[:21]
    y1 = list(fire.get('/A1/Ay', None).values())[:21]
    z1 = list(fire.get('/A1/Az', None).values())[:21]
    timestampA1 = list(fire.get('/A1/Timestamp', None).values())[:21]

    x2 = list(fire.get('/A2/Ax', None).values())[:21]
    y2 = list(fire.get('/A2/Ay', None).values())[:21]
    z2 = list(fire.get('/A2/Az', None).values())[:21]
    timestampA2 = list(fire.get('/A2/Timestamp', None).values())[:21]

    locations = pd.DataFrame(
        {'latitude': lat, 'longitude': lon, 'timestamp': timestampG})
    A1 = pd.DataFrame({'x1': x1, 'y1': y1, 'z1': z1, 'timestamp': timestampA1})
    A2 = pd.DataFrame({'x2': x2, 'y2': y2, 'z2': z2, 'timestamp': timestampA2})

    def convert(timestamp):
        utc = datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
        return (utc + timedelta(hours=5, minutes=30))

    A1.timestamp = A1.timestamp.map(convert).astype(str)
    A2.timestamp = A2.timestamp.map(convert).astype(str)
    A = A1.merge(A2, on=['timestamp'], how='inner')

    locations.timestamp = locations.timestamp.map(lambda k: k.split('.')[0])

    data = A.merge(locations, on=['timestamp'], how='inner')

    def reduce(row):
        row['x'], row['y'], row['z'] = mean([row.x1, row.x2]), mean(
            [row.y1, row.y2]), mean([row.z1, row.z2])
        return (row)

    data = data.apply(reduce, axis=1)

    cols = data.columns.tolist()
    cols = [cols[3]] + cols[9:12] + cols[7:9]
    data = data.ix[:, cols]

    data.to_csv(os.path.join(settings.MEDIA_ROOT, 'data.csv'),
                sep=',', encoding='utf-8')
