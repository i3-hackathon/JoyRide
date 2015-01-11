#!/usr/bin/env python

from collections import defaultdict
tweetsGenerated = defaultdict(lambda: [])

def getId(data):
    return data['TripID'] + " " + data['UserID']

def new_trip(data):
    '''no tweets about the trip yet'''
    tripid = data['TripID']
    history = data['History']
    return len(tweetsGenerated[getId(data)]) == 0

def trip_a_bit_old(data):
    history = data['History']
    # if it's more than one minute old, return True
    return history[0]['Timestamp'] < data['Timestamp'] - 60

def get_recent_destination(data):
    for datum in reversed(data['History']):
        if datum['EventID'] == 7:
            return datum['CarDestination']
    return None

def get_recent_photo(data):
    for datum in reversed(data['History']):
        if datum['EventID'] == 3:  # picture taken
            return datum['PictureLoc']
    return None

def tweet_with_photo_exists(data):
    for old_tweet_list in tweetsGenerated[getId(data)]:
        for old_tweet in old_tweet_list:
            if data['PictureLoc'] == old_tweet['PictureLoc']:
                return True
    return False

def process(data):
    ''' data is a validated JSON-parsed dictionary. Contains all the data
    in BrocaReceiveMessage, in addition to POI, Weather, and Trip history data.

    Returns a list of potential posts in SinglePostFormat.
    '''

    timestamp = data['Timestamp']
    candidate_posts = []

    if new_trip(data) and trip_a_bit_old(data):
        # Make a start of trip tweet
        if 'PictureLoc' not in data or not data['PictureLoc']:
            recent_photo = get_recent_photo(data)
            if recent_photo:
                data['PictureLoc'] = recent_photo

        destination = get_recent_destination(data)

        if destination:
            candidate_posts.append(MakeSinglePostFormat('Starting my road trip to {}!'.format(destination), data))
            candidate_posts.append(MakeSinglePostFormat('Starting my road trip to {} for some hiking! Can\'t wait!'.format(destination), data))
        else:
            candidate_posts.append(MakeSinglePostFormat('Starting my road trip!', data))

    if 'POI' in data and 'PictureLoc' in data:
        candidate_posts.append(MakeSinglePostFormat('Check out my photo at {}!'.format(data['POI']), data))

    if 'POI' in data:
        candidate_posts.append(MakeSinglePostFormat('Looking forward to a lovely evening at {}'.format(data['POI']), data))

    if 'PictureLoc' in data and not tweet_with_photo_exists(data):
        candidate_posts.append(MakeSinglePostFormat('Check out my photo!', data))

    tweetsGenerated[getId(data)].append(candidate_posts)

    return candidate_posts

def MakeSinglePostFormat(text, data):
    return {
        'PostText' : '{} #BMWJoyRide'.format(text),
        'PictureLoc' : data['PictureLoc'] if 'PictureLoc' in data else '',
        'GPS' : data['PhoneGPS'],
        'PostingService' : ['Twitter'],
    }
