#!/usr/bin/env python

def process(data):
    ''' data is a validated JSON-parsed dictionary. Contains all the data
    in BrocaReceiveMessage, in addition to POI, Weather, and Trip history data.
    
    Returns a list of potential posts in SinglePostFormat.
    '''
    
    candidate_posts = [MakeSinglePostFormat('yay', data)]
    
    
    return candidate_posts

def MakeSinglePostFormat(text, data):
    return {
        'PostText' : text,
        'PictureLoc' : data['PictureLoc'] if 'PictureLoc' in data else '',
        'GPS' : data['PhoneGPS'],
        'PostingService' : ['Twitter'],
    }