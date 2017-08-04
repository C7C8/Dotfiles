#!/usr/bin/python3
import json
from urllib import request
from datetime import datetime
from datetime import timedelta
from dateutil import parser as dateParser
from xml.etree import ElementTree
import requests


def get_current_weather(dayCount, latitude, longitude):
    """Query the NOAA's Digital Forecast Database (NDFD) web service to get a dict containing the max/min
    temperature and humidity, the apparent temperature, the relative humidity, weather conditions, and
    various advisories, warnings, and watches, all with matching datetime objects. Parameters are the number of
    future days to grab data for, the latitude, and the longitude, respectively."""
    #TODO Save to geolocation file, update once daily (cron?)

    #ipinfo_raw = urllib.request.urlopen("http://ipinfo.io/json");
    #ipinfo = json.loads(ipinfo_raw.read()) 
    #location = ipinfo["loc"].split(",")
    #print(location)

    weatherArgs = {"lat":latitude,
                   "lon":longitude,
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

    # Extract bulk data; hazards and weather require special handling
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
        if weatherCondition.tag != "weather-conditions":
            continue
        condition = []
        for value in weatherCondition:
            condition.append({"coverage": value.attrib["coverage"],
                              "intensity": value.attrib["intensity"],
                              "weather-type": value.attrib["weather-type"]})
        conditionList.append(condition)
    weather["weather-conditions"] = {"time":weatherParams.find("weather").attrib["time-layout"],
                                     "data":conditionList
    # Hazards
    hazardList = []
    for hazard in weatherParams.find("hazards"):
        if hazard.tag == "hazard-conditions" and hazard.text != None:
            hazardList.append(hazard.text)
    weather["hazards"] = {"time": weatherParams.find("hazards").attrib["time-layout"], "data":hazardList}

    # Splice timelayout into weather
    for key in weather:
        weather[key]["time"] = timeLayouts[weather[key]["time"]]

    weather["daycount"] = dayCount + 1
    return weather

def getDailyMaxTemp(weather):
    """Return a list containing daily max temperatures for the assigned days. If the number of measurements
    does not match the number of days data was collected for, insert nan into the beginning as needed."""
    tempList = weather["temperature:maximum"]["data"]
    while len(tempList) < weather["daycount"]:
        tempList.insert(0, float("nan"))
    return tempList

def getDailyMinTemp(weather):
    """Return a list containing daily min temperatures for the assigned days. If the number of measurements
    does not match the number of days data was collected for, insert nan into the beginning as needed."""
    tempList = weather["temperature:minimum"]["data"]
    while len(tempList) < weather["daycount"]:
        tempList.insert(0, float("nan"))
    return tempList

def getCurrApparentTemp(weather):
    """Returns current apparent temperature"""
    return weather["temperature:apparent"]["data"][0]

def getCurrHumidity(weather):
    """Returns the current relative humidity, as a percentage"""
    return weather["humidity:relative"]["data"][0]

def getMaxHumidity(weather):
    """Returns a list containing daily max humidities for the assigned days. If the number of measurements
    does not match the number of days data was collected for, insert nan into the beginning as needed."""
    humidList = weather["humidity:maximum relative"]["data"]
    while len(humidList) < weather["daycount"]:
        humidList.insert(0, float("nan"))
    return humidList

def getMinHumidity(weather):
    """Returns a list containing daily min humidities for the assigned days. If the number of measurements
    does not match the number of days data was collected for, insert nan into the beginning as needed."""
    humidList = weather["humidity:minimum relative"]["data"]
    while len(humidList) < weather["daycount"]:
        humidList.insert(0, float("nan"))
    return humidList

def weatherGreaterThan(w1, w2):
    """Compare weathers; returns true if w1 is worse than w2, false otherwise."""
    # This function and the next function are both terrible. Sorry!
    weatherTypes = {"": 0, "clear":1, "rain showers":2, "thunderstorms":3, "snow":4}
    return weatherTypes[w1] > weatherTypes[w2]

def chanceGreaterThan(c1, c2):
    """Compare weather chances. returns true if c1 is greater than c2, false otherwise."""
    chanceTypes = {"": 0, "slight chance":1, "chance":2, "likely":3}
    return chanceTypes[c1] > chanceTypes[c2]

def getWeatherType(weather):
    """Returns a list containing the weather for a day coupled to its chance. Daily weather is defined by the
    worst weather type with a coverage chance of 'chance'.

    Note that, since the NDFD data time layout doesn't correspond to the actual data here AT ALL, this
    function is *probably* borked."""
    weatherList = []
    currentDay = weather["weather-conditions"]["time"][0][0].day
    if datetime.now().day != currentDay:
        weatherList.append(["",""])
    worstWeather = ""
    chance = ""
    for i in range(len(weather["weather-conditions"]["time"][0])):
        if weather["weather-conditions"]["time"][0][i].day != currentDay:
                weatherList.append([worstWeather, chance])
                worstWeather = ""
                chance = ""
                currentDay = weather["weather-conditions"]["time"][0][i].day

        for condition in weather["weather-conditions"]["data"][i]:
            currWeather = condition["weather-type"]
            currChance = condition["coverage"]
            if weatherGreaterThan(currWeather, worstWeather) and chanceGreaterThan(currChance, chance):
                worstWeather = currWeather
                chance = currChance

    return weatherList


weather = get_current_weather(2, NOPE, NOPE)
print(getDailyMaxTemp(weather))
print(getDailyMinTemp(weather))
print(getCurrApparentTemp(weather))
print(getCurrHumidity(weather))
print(getMaxHumidity(weather))
print(getMinHumidity(weather))
print(weather["weather-conditions"]["time"])
for data in getWeatherType(weather):
    print(data)
