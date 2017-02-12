# Get weather conditions through WeatherUnderground (based on:
# https://www.hackster.io/brad-buskey/getweather-for-omega2-8e3298)
import json
import urllib2
import numpy as np

import config as cg

# WUnderground API (https://www.wunderground.com/weather/api)
apikey = cg.read_ini('WU', 'apikey', filename='secret')
lat = cg.read_ini('WU', 'lat', filename='secret')
lon = cg.read_ini('WU', 'lon', filename='secret')
cg.send('> WU - Key {} / GPS ({}, {})'.format(apikey, lat, lon))


def fetch(req_type):
    """Request Weather Data"""
    GetURL = "http://api.wunderground.com/api/" + apikey + \
        "/{}/q/{},{}.json".format(req_type, lat, lon)
    weatherdict = urllib2.urlopen(GetURL).read()
    weatherinfo = json.loads(weatherdict)
    # print '\nComplete weatherinfo JSON:'
    # print weatherinfo
    return weatherinfo


def conditions():
    """Get the day's summary"""
    weatherinfo = fetch('conditions')
    # For current conditions, everything is under current observation:
    weatherdata = weatherinfo['current_observation']

    weather = weatherdata['weather']  # Overcast
    temperature_string = weatherdata['temperature_string']  # 37.0 F (2.8 C)
    temp_c = weatherdata['temp_c']  # 2.8
    feelslike_c = weatherdata['feelslike_c']  # 4
    windchill_c = weatherdata['windchill_c']  # 3
    wnd = weatherdata['wind_string']  # From the South at 2.0 MPH...
    wind_gust_mph = weatherdata['wind_gust_mph']  # 7.0
    precip = weatherdata['precip_today_string']  # 0.00 in (0 mm)
    precip_1hr_metric = weatherdata['precip_1hr_metric']  # 0.00
    precip_today_metric = weatherdata['precip_today_metric']  # 0
    relative_humidity = weatherdata['relative_humidity']  # 40%

    return {
        "weather": weather,
        "temperature_string": temperature_string,
        "temp_c": temp_c,
        "feelslike_c": feelslike_c,
        "windchill_c": windchill_c,
        "wnd": wnd,
        "wind_gust_mph": wind_gust_mph,
        "precip": precip,
        "precip_1hr_metric": precip_1hr_metric,
        "precip_today_metric": precip_today_metric,
        "relative_humidity": relative_humidity
    }


def forecast():
    weatherinfo = fetch('forecast')
    print weatherinfo
    print "Error: forecast....isn't parsed yet"


def hourly(quiet=True):
    """Get hourly data for a 36 hour window"""
    weatherinfo = fetch('hourly')
    weatherdata = weatherinfo['hourly_forecast']
    if not quiet:
        # print weatherdata[0]
        print '\n Forecast for {} hours \n'.format(len(weatherdata))

    # Determine the morning commute weather and when I would commute home
    hours = [x['FCTTIME']['hour'] for x in weatherdata]
    commute_weather = []
    # For morning (0) and afternoon (8)
    for i in [0, 8]:
        hour, fc, cnd, temp, tmp = [], [], [], [], []
        wspd, wdir = [], []
        pop, hm, snow, qpf = [], [], [], []
        # Three hour window for each
        for j in [0, 1, 2]:
            k = i + j + hours.index('5')  # Start everything at 5 am
            hour = weatherdata[k]  # 15
            fc.append(hour['wx'])  # Clear/Wind
            cnd.append(hour['condition'])  # Chance of Rain
            temp.append(eval(hour['temp']['metric']))  # 9
            tmp.append(eval(hour['feelslike']['metric']))  # 9
            # wspd.append(eval(hour['wspd']['metric']))  # 37
            wspd.append(eval(hour['wspd']['english']))  # 20
            wdir.append(hour['wdir']['dir'])  # WNW
            # wchl.append(eval(hour['windchill']['metric']))  # 9
            pop.append(eval(hour['pop']))  # 30 {prob of precip}
            hm.append(eval(hour['humidity']))  # 46
            snow.append(eval(hour['snow']['metric']))  # 0
            qpf.append(eval(hour['qpf']['metric']))  # 0 {rain?}
        commute_weather.append({
            "fc": fc[1],
            "cnd": cnd[1],
            "temp": '{:3.1f}C'.format((np.mean(temp))),
            "tmp": '{:+d}C'.format(int(np.mean(tmp))),
            "wspd": '{:2d} mph'.format(int(np.mean(wspd))),
            "wdir": wdir[1],
            "pop": np.amax(pop),
            "hm": '{:2d}%'.format(int(np.mean(hm))),
            "snow": '{} cm'.format(np.amax(snow)),
            "precip": np.amax(qpf)
        })
    return commute_weather
