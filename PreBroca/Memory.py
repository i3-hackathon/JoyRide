#!/usr/bin/env python
'''Store a history of data about a trip. This history contains all the PreBroca
data except for event history. '''

from collections import defaultdict
histories = defaultdict(lambda: [])

def getId(data):
    return data['TripID'] + " " + data['EventID']

def addHistory(data):
    '''data is a validated JSON-parsed dictionary. Data is mutable, so we add the field
    'history' to 'data' itself. On failure, do nothing.

    'history' is a list of extended BasicEventMessageContent items. Extended here
    means that in addition to the usual fields, it has the 'POI', 'HAMWeather', and
    'WeatherUnderground' fields. '''
    history = histories.get(getId(data))
    data['history'] = history

def store(data):
    '''data is a validated JSON-parsed dictionary.'''
    history = histories.get(getId(data))
    history.append(data)
