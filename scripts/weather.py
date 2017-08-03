#!/usr/bin/python3
import json
from urllib import request
from datetime import datetime
from datetime import timedelta
from dateutil import parser as dateParser
from xml.etree import ElementTree
import requests


def get_current_weather():
    #TODO Save to geolocation file, update once daily (cron?)

    #ipinfo_raw = urllib.request.urlopen("http://ipinfo.io/json");
    #ipinfo = json.loads(ipinfo_raw.read()) 
    #location = ipinfo["loc"].split(",")
    #print(location)

    weatherArgs = {"lat":NOPE,
                   "lon":NOPE,
                   "product":"time-series",
                   "begin":datetime.utcnow().isoformat(),
                   "end":(datetime.utcnow() + timedelta(days = 2)).isoformat(),
                   "Unit":"e",
                   "format":"24 hourly",
                   "maxt":"maxt",
                   "mint":"mint",
                   "appt":"appt",
                   "snow":"snow",
                   "rh":"rh",
                   "wx":"wx",
                   "wwa":"wwa",
                   "maxrh":"maxrh",
                   "minrh":"minrh"}
    #weatherDataRaw = requests.get("https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php", weatherArgs).text
    #weatherTreeRoot = ElementTree.fromstring(weatherDataRaw).find("data")
    weatherTreeRoot = ElementTree.parse("output.xml").getroot().find("data")

    timeLayouts = {}
    weather = {}

    # First get available time ranges, stored by key of layout-key and a list of tuples of datetimes.
    for timeLayout in weatherTreeRoot.findall("time-layout"):
        layoutKey = timeLayout.find("layout-key").text
        rangeList = []
        cur = []
        for child in timeLayout:
            if child.tag == "layout-key":
                continue
            cur.append(dateParser.parse(child.text))
            if child.tag == "end-valid-time":
                rangeList.append(cur)
                cur = []

        if len(cur) > 0:
            rangeList.append(cur)
        timeLayouts[layoutKey] = rangeList
        rangeList = []

    # Extract bulk data, hazards and weather require special handling
    weatherParams = weatherTreeRoot.find("parameters")
    for datatype in weatherParams:
        if datatype.tag == "time-layout" or datatype.tag == "weather" or datatype.tag == "hazards":
            continue

        paramName = datatype.tag + ":" + datatype.attrib["type"]
        data = []
        for point in datatype.findall("value"):
            data.append(float(point.text))
        weather[paramName] = {"time":datatype.attrib["time-layout"], "data":data}

    # Weather
    conditionList = []
    for weatherCondition in weatherParams.find("weather"):
        condition = []
        for value in weatherCondition:
            condition.append({"coverage": value.attrib["coverage"],
                              "intensity": value.attrib["intensity"],
                              "weather-type": value.attrib["weather-type"]})
            if len(condition) > 0:
                conditionList.append(condition)
    weather["weather-conditions"] = {"time":weatherParams.find("weather").attrib["time-layout"],
                                     "data":conditionList}

    # Hazards
    hazardList = []
    for hazard in weatherParams.find("hazards"):
        if hazard.tag == "hazard-conditions" and hazard.text != None:
            hazardList.append(hazard.text)
    weather["hazards"] = {"time": weatherParams.find("hazards").attrib["time-layout"], "data":hazardList}

    # Splice timelayout into weather
    for key in weather:
        weather[key]["time"] = timeLayouts[weather[key]["time"]]

    return weather


print(get_current_weather())
