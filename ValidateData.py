#!/usr/bin/env python

def validate(data, MessageFormats):
    '''Returns True if data fits MessageFormat, else returns an error string.
    
    data is a JSON-parsed dictionary. MessageFormats is a dictionary keyed by event ID.
    The value is a dictionary where the key is the required data field, and the value is either
    a function that returns true on a correctly formatted data or a data type. '''
    try:
        if 'EventID' not in data:
            return 'No EventID.'
        MessageFormat = MessageFormats[data['EventID']]
        check = validate_message_format(data, MessageFormat)
        if check is not True:
            return check
        
    except Exception as e:
        return 'Message malformed.'

    return True

def validate_message_format(data, MessageFormat):
    # Validator is either the expected variable type or a function that returns true if
    # the variable is correctly formed.
    for key, validator in MessageFormat.items():
        # validator is a validating function.
        try:
            if not validator(data_to_validate = data[key]):
                return "Key '%s' is not formatted correctly."%(key,)
        # validator is a variable type
        except:
            if not type(data[key]) == validator:
                return 'Key %s is not formatted correctly.'%(key,)
    return True
    