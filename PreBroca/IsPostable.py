PostableReasons = {
    1 : 'Any picture is taken',
    2 : 'Near famous thing and stopped at all',
    3 : 'Stopped for more than 30 min'
}

def EventIsPostable(data):
    ''' Returns true if we should generate candidate tweets. If so, include the
    triggering reason by mutating 'data'. '''
    return True
    if 'PictureLoc' in data: # Picture taken
        data['TriggerCondition'] = 1
        return True
    elif data['EventID'] == 11: # Car off
        pass
    elif data['EventID'] == 2: # Car MPH is super low
        pass
    
    
    return False