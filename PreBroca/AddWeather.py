#!/usr/bin/env python
'''Add Weather data to the message before it gets passed to Broca.

Gets from HAMWeather and Weather Underground.'''

import logging

# For HAMWeather
import urllib2
import json

def add(data):
    '''data is a validated JSON-parsed dictionary. Data is mutable, so we add the field
    to 'data' itself. On failure, do nothing. '''
    try:
        AddHAMWeather(data)
    except Exception as e:
        logging.info(e)
    try:
        AddWeatherUnderground(data)
    except Exception as e:
        logging.info(e)

client_id = 'cTJ0wNlmYFBBeeeI9xPkb'
client_secret = 'PkyOUIcW3C00mSu1npSQy53t3RaXMe3wB6wVjMst'
def AddHAMWeather(data):
    request = urllib2.urlopen('http://api.aerisapi.com/observations/seattle,wa?' +
                              'client_id=%s&client_secret=%s'%(client_id, client_secret))
    response = request.read()
    resp = json.loads(response)
    if resp['success']:
       data['Weather'] = resp['response']['ob']
       #print ob
       #print "The current weather in Seattle is %s with a temperature of %d" % (ob['weather'].lower(), ob['tempF'])
    request.close()

def AddWeatherUnderground(data):
    pass
