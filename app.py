#!/usr/bin/python
from flask import Flask, request, render_template
import datetime
from requests import get

app = Flask(__name__)

key = "403767acba3af3e7dadf1121586b5f8d"
app_id = "00d644e1"

def getAtcoCodes(postcode):
    assert postcode == 'NW51TL'
    return ['490008660N','490008660S']

def parseResponse(busResponse):
    upcomingBuses = []
    for lineBuses in busResponse['departures'].values():
        for upcomingBus in lineBuses:
            upcomingBuses += [
                {
                    "busStop": busResponse['name'],
                    "lineNumber": upcomingBus['line'],
                    "direction": upcomingBus['direction'],
                    "expectedDepartureTime": upcomingBus['best_departure_estimate']
                }
            ]
    return upcomingBuses

def listSort(e):
    return e['expectedDepartureTime']


@app.route('/')
def display_bus_info():
    resp = []
    for code in getAtcoCodes('NW51TL'):
        url = 'http://transportapi.com/v3/uk/bus/stop/' + code + '/live.json'
        print(url)
        busResponse = get(url, params={ 'app_id':app_id,  'app_key' : key})
        resp += parseResponse(busResponse.json())
    resp.sort(key=listSort)
    return render_template('index.html', upcomingBuses=resp, timeStamp=datetime.datetime.now())
