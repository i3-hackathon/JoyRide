#!/usr/bin/env python
'''Store a history of data about a trip. This history contains all the PreBroca
data except for event history. '''

def addHistory(data):
    '''data is a validated JSON-parsed dictionary. Data is mutable, so we add the field
    'history' to 'data' itself. On failure, do nothing.
    
    'history' is a list of extended BasicEventMessageContent items. Extended here
    means that in addition to the usual fields, it has the 'POI', 'HAMWeather', and
    'WeatherUnderground' fields. '''
    pass

def store(data):
    '''data is a validated JSON-parsed dictionary.'''
    pass