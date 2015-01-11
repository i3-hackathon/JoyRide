#!/usr/bin/env python

from ValidateData import validate_message_format

EventIDDescription = {
    1 : "Query user for start of trip",
    2 : "Query user for end of trip",
    3 : "Submit potential posts to user",
    4 : "General user query",
}
def IsCoordinates(data_to_validate):
    return type(data_to_validate) is list and \
           len(data_to_validate) is 2 and \
           type(data_to_validate[0]) is float and \
           type(data_to_validate[1]) is float
        
def IsPostingService(data_to_validate):
    if type(data_to_validate) is not list:
        return False
    for item in data_to_validate:
        if type(item) is not str:
            return False
    return True

SinglePostFormat = {
    'PostText' : str,
    'PictureLoc' : str,
    'GPS' : IsCoordinates,
    'PostingService' : IsPostingService,
}

def IsSinglePostFormatList(data_to_validate):
    if type(data_to_validate) is not list:
        return False
    for list_item in data_to_validate:
        if validate_message_format(list_item, SinglePostFormat) is not True:
            return False
    return True

# Values are either the type or a function that returns true if the type if correct.
CandidatePostMessage = {
    'EventID' : int,
    'PostData' : IsSinglePostFormatList, # Doesn't have to have this if querying the user.
    'Timestamp' : int,
}

QueryUserMessage = {
    'EventID' : int,
    'Timestamp' : int,
}

# Used by ValidateData.validate
EventMessageFormat = {
    1 : QueryUserMessage,
    2 : QueryUserMessage,
    3 : CandidatePostMessage,
    4 : QueryUserMessage,
}