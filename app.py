#!/usr/bin/python
from flask import Flask, request, render_template
from requests import get

app = Flask(__name__)

key = "403767acba3af3e7dadf1121586b5f8d"
app_id = "00d644e1"

def getAtcoCodes(postcode):
    assert postcode == 'NW51TL'
    return ['490008660N','490008660S']

@app.route('/')
def display_bus_info():
    resp = []
    for code in getAtcoCodes('NW51TL'):
        url = 'http://transportapi.com/v3/uk/bus/stop/' + code + '/live.json'
        print(url)
        bus_response = get(url, params={ 'app_id':app_id,  'app_key' : key})
        resp += [bus_response.json()]
    return str(resp)
