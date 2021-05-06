#!/usr/bin/python
from flask import Flask, request, render_template
from requests import get

app = Flask(__name__)

key = "403767acba3af3e7dadf1121586b5f8d"
app_id = "00d644e1"

def getAtcoCodes(postcode):
    assert postcode == 'NW51TL'
    url = 'http://api.postcodes.io/postcodes/' + postcode
    print(url)
    resp = get(url).json()
    longitude = resp.get('result').get('longitude')
    latitude = resp.get('result').get('latitude')
    print(longitude)
    print(latitude)
 
    url = 'http://transportapi.com/v3/uk/places.json'
    codes_response = get(url, params={ 'app_id':app_id,  'app_key' : key, 'lat' : latitude, 'lon' : longitude, 'type' : 'bus_stop'})
    print(codes_response.json())
    bus_stop_list = codes_response.json().get('member')
    bus_stop1 = bus_stop_list[0].get('atcocode')
    bus_stop2 = bus_stop_list[1].get('atcocode')
    print(bus_stop1)
    print(bus_stop2)
    
    return [bus_stop1,bus_stop2]

@app.route('/')
def display_bus_info():
    resp = []
    for code in getAtcoCodes('NW51TL'):
        url = 'http://transportapi.com/v3/uk/bus/stop/' + code + '/live.json'
        print(url)
        bus_response = get(url, params={ 'app_id':app_id,  'app_key' : key})
        resp += [bus_response.json()]
    return str(resp)
