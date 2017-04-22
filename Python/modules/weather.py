# Get weather conditions through WeatherUnderground (based on:
# https://www.hackster.io/brad-buskey/getweather-for-omega2-8e3298)
import json
import random
import urllib2
import numpy as np

import config as cg


class WUnderground():
    # WUnderground API (https://www.wunderground.com/weather/api)
    count = 0

    def __init__(self):
        self.apikey = cg.read_ini('WU', 'apikey', filename='secret')
        self.lat = cg.read_ini('WU', 'lat', filename='secret')
        self.lon = cg.read_ini('WU', 'lon', filename='secret')
        cg.send('> WU - Key {} / GPS ({}, {})'.format(
            self.apikey, self.lat, self.lon))

    def fetch(self, req_type):
        """Request Weather Data"""
        GetURL = "http://api.wunderground.com/api/" + self.apikey + \
            "/{}/q/{},{}.json".format(req_type, self.lat, self.lon)
        weatherdict = urllib2.urlopen(GetURL).read()
        weatherinfo = json.loads(weatherdict)
        # cg.send('\nComplete weatherinfo JSON:')
        # cg.send(weatherinfo)
        self.count += 1
        cg.send('New WU request, total: {}'.format(self.count))
        return weatherinfo


# Make sure this is only called once.
WU = WUnderground()


def conditions():
    """Get the day's summary"""
    weatherinfo = WU.fetch('conditions')
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
    weatherinfo = WU.fetch('forecast')
    print weatherinfo
    print "Error: forecast....isn't parsed yet"


def hourly(quiet=True):
    """Get hourly data for a 36 hour window"""
    weatherinfo = WU.fetch('hourly')
    weatherdata = weatherinfo['hourly_forecast']

    # Determine the morning commute weather and for when I commute home
    hours = [x['FCTTIME']['hour'] for x in weatherdata]
    commute_weather = []
    # window = 3  # hours
    window = 2  # hours
    # For morning (0) and afternoon (8)
    for i in [0, 8]:
        k_init = False
        wspd, wdir = [], []
        pop, hm, snow, qpf = [], [], [], []
        hour, fc, cnd, temp, tmp = [], [], [], [], []
        # Three hour window for each
        for j in range(window):
            # **Keep weather up to date up to 8 am of the same day
            hi = hours.index('8') - window
            k = i + j + (hi)  # sort of solve for 5 am
            cg.send('Starting loop j:{}+i:{}+hi:{} = k:{} (k_init={})'.format(
                    j, i, hi, k, k_init))
            k = k if k > 0 else 0
            hour = weatherdata[k]
            if type(k_init) is not int:
                ts_start = hour['FCTTIME']['pretty']
                h_start = hour['FCTTIME']['hour']
                day = hour['FCTTIME']['weekday_name_abbrev']
                k_init = k
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
        # "snow": '{} cm'.format(np.amax(snow)),
        commute_weather.append({
            "ts": ts_start,
            "hr": h_start,
            "day": day,
            "fc": fc[1],
            "cnd": cnd[1],
            "temp": '{:3.1f}C'.format((np.mean(temp))),
            "tmp": '{:+d}C'.format(int(np.mean(tmp))),
            "wspd": '{}mph'.format(int(np.mean(wspd))),
            "wdir": wdir[1],
            "pop": '{}%'.format(np.amax(pop)),
            "hm": '{:2d}%'.format(int(np.mean(hm))),
            "snow": 'SNOW! ' if np.amax(snow) > 0.1 else '',
            "precip": np.amax(qpf)
        })
    # cg.send('Example (Wthr cnd):', commute_weather[0]["cnd"])
    if not quiet:
        # _r = random.randint(0, len(commute_weather) - 1)  # used to be rand
        _r = 0  # now just the first
        # cg.send('commute_weather[{}]: {}'.format(_r, commute_weather[_r]))
        cg.send('weather[{}][ts]= {}'.format(_r, commute_weather[_r]["ts"]))
    return commute_weather
