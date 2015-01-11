#!/usr/bin/env python

EventIDDescription = {
    1 : "Car on",
    11 : "Car off",
    2 : "Car MPH is 0",
    3 : "Picture taken",
    4 : "Car is slow",
    5 : "Car is fast",
    6 : "Heartbeat",
    7 : "Car destination is set",
    8 : "User confirms that trip has started",
    9 : "User confirms that trip has ended",
    10 : "User confirms that she wants to post",
}

def IsCoordinates(data_to_validate):
    return type(data_to_validate) is list and \
           len(data_to_validate) is 2 and \
           type(data_to_validate[0]) is float and \
           type(data_to_validate[1]) is float

def IsFloatOrInt(data_to_validate):
    return type(data_to_validate) is float or type(data_to_validate) is int

def IsCoordinatesOrNone(data_to_validate):
    return data_to_validate is None or IsCoordinates(data_to_validate)

# Values are either the type or a function that returns true if the type if correct.
BasicEventMessageContent = {
    'EventID': int,
    'TripID': int,  # -1 means that there is no trip
    'UserID': unicode,
    'CarMPH': IsFloatOrInt,
    'CarGPS': IsCoordinates,
    'PhoneGPS': IsCoordinates,
    'CarWeather': IsFloatOrInt,
    'Temperature': IsFloatOrInt,
    'CarDestination': IsCoordinatesOrNone,
    'Timestamp': int,
}

RequestCandidateTweetsMessageContent = {
    'EventID': int,
    'TripID': int,  # -1 means that there is no trip
    'UserID': unicode,
    'Timestamp': int,
}

'''
UserConfirmationMessageContent = {
    'EventID': int,
    'TripID': int,
    'UserID': unicode,
    'Response': unicode,
    'Timestamp': int,
}'''

# Used by ValidateData.validate
EventMessageFormat = {
    1 : BasicEventMessageContent,
    11 : BasicEventMessageContent,
    2 : BasicEventMessageContent,
    3 : dict(BasicEventMessageContent, PictureLoc = str),
    4 : BasicEventMessageContent,
    5 : BasicEventMessageContent,
    6 : BasicEventMessageContent,
    7 : BasicEventMessageContent,
    #8 : UserConfirmationMessageContent,
    #9 : UserConfirmationMessageContent,
    #10 : UserConfirmationMessageContent,
    12 : RequestCandidateTweetsMessageContent,
}
