#!/usr/bin/env python

import socket
import json

good_data1 = {
    'EventID': 1,
    'TripID': 2,
    'UserID': 'joel.ivan@google.com',
    'CarMPH': 2.43,
    'CarGPS': [1.2, 2.3],
    'PhoneGPS': [1.24, 2.34],
    'CarWeather': 2.34,
    'Temperature': 65.2,
    'CarDestination': [-1.23, 6.34],
    'Timestamp': 1232,
}
'''
good_data2 = {
    'EventID': 8,
    'TripID': 2,
    'UserID': 'joel.ivan@google.com',
    'Response': 'Please send it!',
    'Timestamp': 1232,
}'''
good_data3 = {
    'EventID': 1,
    'TripID': -1,
    'UserID': 'joel.ivan@google.com',
    'CarMPH': 2.43,
    'CarGPS': [1.2, 2.3],
    'PhoneGPS': [1.24, 2.34],
    'CarWeather': 2.34,
    'Temperature': 65.2,
    'CarDestination': [-1.23, 6.34],
    'Timestamp': 1232,
}
bad_data1 = {'message':'hello world!', 'test':123.4}
bad_data2 = {'EventID':1, 'test':123.4}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(bad_data1))
result = json.loads(s.recv(1024))
print result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(bad_data2))
result = json.loads(s.recv(1024))
print result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(good_data1))
result = json.loads(s.recv(1024))
print result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(good_data3))
result = json.loads(s.recv(1024))
print result

s.close()