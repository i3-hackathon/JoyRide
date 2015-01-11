#!/usr/bin/env python
'''Add Weather data to the message before it gets passed to Broca.

Gets from HAMWeather and Weather Underground.'''

def add(data):
    '''data is a validated JSON-parsed dictionary. Data is mutable, so we add the field
    to 'data' itself. On failure, do nothing. '''
    AddHAMWeather(data)
    AddWeatherUnderground(data)

def AddHAMWeather(data):
    pass

def AddWeatherUnderground(data):
    pass