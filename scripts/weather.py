#!/usr/bin/python3
import json
from urllib import request
from datetime import datetime
from datetime import timedelta
from xml.etree import ElementTree
from suds.client import Client as SudsClient


def get_current_weather():
    #TODO Save to geolocation file, update once daily (cron?)

    #ipinfo_raw = urllib.request.urlopen("http://ipinfo.io/json");
    #ipinfo = json.loads(ipinfo_raw.read()) 
    #location = ipinfo["loc"].split(",")
    #print(location)

    noaaClient = SudsClient("https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl")
    #Max/mintemp, snowfall, humidity, wind speed, watches, warnings, advisories, weather, min/max humidity
    weatherParams = {"latitude": nope,
                      "longitude": nope,
                      "product": "time-series",
                      "endTime": (datetime.now() + timedelta(days=2)).strftime("%c"), 
                      "Unit": "e"} # imperial, use m for metric
    print(weatherParams)
    weatherDataRaw = noaaClient.service.NDFDgen(**weatherParams)
    print(weatherDataRaw)


    #weathertree = ElementTree.fromstring(weather_data)

get_current_weather()
