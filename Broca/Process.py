#!/usr/bin/env python

def process(data):
    ''' data is a validated JSON-parsed dictionary. Contains all the data
    in BrocaReceiveMessage, in addition to POI, Weather, and Trip history data.

    Returns a list of potential posts in SinglePostFormat.
    '''

    candidate_posts = []

    if 'POI' in data and 'PictureLoc' in data:
        candidate_posts.append(MakeSinglePostFormat('Check out my photo at {}!'.format(data['POI']), data))

    if 'POI' in data:
        candidate_posts.append(MakeSinglePostFormat('Looking forward to a lovely evening at {}'.format(data['POI']), data))

    if 'PictureLoc' in data:
        candidate_posts.append(MakeSinglePostFormat('Check out my photo!', data))


    return candidate_posts

def MakeSinglePostFormat(text, data):
    return {
        'PostText' : '{} #BMWJoyRide'.format(text),
        'PictureLoc' : data['PictureLoc'] if 'PictureLoc' in data else '',
        'GPS' : data['PhoneGPS'],
        'PostingService' : ['Twitter'],
    }
