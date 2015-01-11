#!/usr/bin/env python
'''Determine whether a trip should start or end. If in the middle of a trip, get additional data for
Broca and add it to message. Then take response and format it correctly. '''

import time
import logging

import AddPOI
import AddWeather
import StoreToTripHistory
import AddTripHistory
import Broca.Process as Broca

def QueryForTripStart():
    return {
        'EventID' : 1,
        'Timestamp' : int(time.time()),
        }

def QueryForTripEnd():
    return {
        'EventID' : 2,
        'Timestamp' : int(time.time()),
        }

def process(data):
    '''data is a validated JSON-parsed dictionary.
    Returns the correctly formatted response message as a BrocaSendMessageFormat.'''
    
    if data['TripID'] == -1:
        if TripMightBeStarting(data) is True:
            logging.info('Trip might be starting')
            return QueryForTripStart()
        
    AddPOI.add(data)
    AddWeather.add(data)
    AddTripHistory.add(data)
    
    if TripMightBeEnding(data):
        return QueryForTripEnd()
    
    # Broca returns a list of candidate posts in SinglePostFormat.
    logging.info('About to enter Broca')
    candidate_posts = Broca.process(data)
    logging.info('Just left Broca')
    
    return FormatReturnMessage(candidate_posts)

def FormatReturnMessage(candidate_posts):
    ''' Return a BrocaSendMessageFormat from a list of SinglePostFormat objects.'''
    return {
        'EventID' : 3, # This means candidate posts
        'PostData' : candidate_posts,
        'Timestamp' : int(time.time()),
    }

def TripMightBeStarting(data):
    ''' Returns True if the user is not in a trip, but the data suggests that one might be starting. '''
    return True

def TripMightBeEnding(data):
    return False