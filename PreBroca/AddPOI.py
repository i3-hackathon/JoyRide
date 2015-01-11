#!/usr/bin/env python
'''Add POI data to the message before it gets passed to Broca.

Use HERE Places API. Specifically, it looks like this:
List of:
{
    'title': str,
    'id': str,
    'distance': int,
    'categories': list[str],
    'ratings average': float,
    'ratings count': int,
}
'''

default_POI = {
    'title': 'Big Sur Campground & Cabins',
    'id': '8409q3qk-3c8d8c885b824cb192651cd286f3a2b4',
    'distance': 1,
    'categories': ['hotel'],
    'ratings average': 0,
    'ratings count': None,
}

POIs_by_location = {
    # 37, -122:
}

def add(data):
    '''data is a validated JSON-parsed dictionary. Data is mutable, so we add the field
    to 'data' itself. On failure, do nothing. '''
    data['POI'] = default_POI
