# Get weather conditions through WeatherUnderground (based on:
# https://www.hackster.io/brad-buskey/getweather-for-omega2-8e3298)
import json
import urllib2

import config as cg

# WUnderground API (https://www.wunderground.com/weather/api)
apikey = cg.read_ini('WU', 'apikey', filename='secret')
lat = cg.read_ini('WU', 'lat', filename='secret')
lon = cg.read_ini('WU', 'lon', filename='secret')
print '> Secret info:', apikey, lat, lon

# Request Weather Data - Pick forecast type:
feature = ['conditions', 'forecast', 'hourly'][2]
GetURL = "http://api.wunderground.com/api/" + apikey + \
    "/{}/q/{},{}.json".format(feature, lat, lon)
weatherdict = urllib2.urlopen(GetURL).read()
weatherinfo = json.loads(weatherdict)
# print '\nComplete weatherinfo JSON:'
# print weatherinfo


if 'conditions' in feature:
    # For current, everything is under current observation:
    weatherdata = weatherinfo['current_observation']

    # Print some example info `print "key (desc): {}".format(key)`:

    cty = weatherdata['display_location']['city']
    sta = weatherdata['display_location']['state']
    loc = cty + ", " + sta
    print "\nloc (Fallsgrove, MD): {}".format(loc)

    weather = weatherdata['weather']
    temperature_string = weatherdata['temperature_string']
    precip = weatherdata['precip_today_string']
    wnd = weatherdata['wind_string']
    print "weather (Overcast): {}".format(weather)
    print "temperature_string (37.0 F (2.8 C)): {}".format(temperature_string)
    print "precip (0.00 in (0 mm)): {}".format(precip)
    print "wnd (From the South at 2.0 MPH Gusting to 7.0 MPH): {}".format(wnd)

    # New
    precip_today_metric = weatherdata['precip_today_metric']
    # 'precip_today_in':'0.00',
    print "precip_today_metric (0): {}".format(precip_today_metric)
    windchill_c = weatherdata['windchill_c']
    print "windchill_c (3): {}".format(windchill_c)
    feelslike_c = weatherdata['feelslike_c']
    print "feelslike_c (3): {}".format(feelslike_c)
    temp_c = weatherdata['temp_c']
    print "temp_c (2.8): {}".format(temp_c)
    wind_gust_mph = weatherdata['wind_gust_mph']
    print "wind_gust_mph (7.0): {}".format(wind_gust_mph)
    precip_1hr_metric = weatherdata['precip_1hr_metric']
    # 'precip_1hr_metric':' 0',
    print "precip_1hr_metric (0.00): {}".format(precip_1hr_metric)
    relative_humidity = weatherdata['relative_humidity']
    print "relative_humidity (40%): {}".format(relative_humidity)

elif 'forecast' in feature:
    print "forecast....isn't parsed yet"

elif 'hourly' in feature:
    weatherdata = weatherinfo['hourly_forecast']
    # print 'Forecast for {} hours'.format(len(weatherdata))
    # Determine the morning commute weather and when I would commute home
    hours = range(len(weatherdata))
    for i, hour in enumerate(weatherdata):
        hours[i] = hour['FCTTIME']['hour']
    for i in [0, 1, 2, 8, 9, 10]:
        k = hours.index('5') + i
        hour = weatherdata[k]
        # print 'h', hour['FCTTIME']['hour']
        fc = hour['wx']
        tmp = hour['feelslike']['metric']
        hm = hour['humidity']
        snow = hour['snow']['metric']
        wchl = hour['windchill']['metric']
        wspd = hour['wspd']['metric']
        wdir = hour['wdir']['dir']
else:
    print feature, "- is not yet parsed"
