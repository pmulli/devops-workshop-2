#!/usr/bin/python
from flask import Flask, request, render_template
import datetime
from requests import get

app = Flask(__name__)

key = "403767acba3af3e7dadf1121586b5f8d"
app_id = "00d644e1"

def getAtcoCodes(postcode):
    #assert postcode == 'NW51TL'
    url = 'http://api.postcodes.io/postcodes/' + postcode
    resp = get(url).json()
    bus_stops = []
    if resp.get('result') != None:
        longitude = resp.get('result').get('longitude')
        latitude = resp.get('result').get('latitude')
        print(longitude)
        print(latitude)
    
        url = 'http://transportapi.com/v3/uk/places.json'
        codes_response = get(url, params={ 'app_id':app_id,  'app_key' : key, 'lat' : latitude, 'lon' : longitude, 'type' : 'bus_stop'})
        bus_stop_list = codes_response.json().get('member')
        bus_stop_list.sort(key=extract_distance, reverse=False)

        bus_stop1 = bus_stop_list[0].get('atcocode')
        bus_stop2 = bus_stop_list[1].get('atcocode')
        bus_stop1_dist = bus_stop_list[0].get('distance')
        bus_stop2_dist = bus_stop_list[1].get('distance')

        print(bus_stop1 + " - " + str(bus_stop1_dist))
        print(bus_stop2 + " - " + str(bus_stop2_dist))

        bus_stops = [bus_stop1,bus_stop2]
    
    return bus_stops

def extract_distance(json):
    try:
        return json['distance']
    except KeyError:
        return 0

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


@app.route('/', methods=['GET', 'POST'])
def display_bus_info():
    postcode = request.form.get('postcode')
    if postcode == None:
        postcode = 'NW51TL'
    print('postcode: ' + postcode)
    resp = []
    for code in getAtcoCodes(postcode):
        url = 'http://transportapi.com/v3/uk/bus/stop/' + code + '/live.json'
        print(url)
        busResponse = get(url, params={ 'app_id':app_id,  'app_key' : key})
        resp += parseResponse(busResponse.json())
    resp.sort(key=listSort)
    return render_template('index.html', postcode=postcode, upcomingBuses=resp, timeStamp=datetime.datetime.now())
