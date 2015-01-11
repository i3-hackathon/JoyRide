#!/usr/bin/env python

import SocketServer
import json
import logging
import traceback

import ValidateData
import PreBroca.Process as PreBroca
from MessageFormats.BrocaReceiveMessageFormat import EventMessageFormat as IncomingFormat
from MessageFormats.BrocaSendMessageFormat import EventMessageFormat as OutgoingFormat

import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

index = 0
responses = [
    """
        [
{
"EventID": 3,
"Timestamp": 100,
"PostData": [
            {
              "PostText": "I just drove over the Golden Gate!",
              "PictureLoc": "http://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            },
            {
              "PostText": "The Golden Gate Bridge is beautiful!",
              "PictureLoc": "http://www.howardmodels.com/fun-stuff/golden-gate-bridge/Golden-Gate-Bridge-Sunset.jpg",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            }
          ]
}
]
        """,

    """
        [
{
"EventID": 3,
"Timestamp": 100,
"PostData": [
            {
              "PostText": "Starting on my road trip to Big Sur. Can't wait!! #BMWJoyRide",
              "PictureLoc": "https://scontent-a.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/10888643_10152913233001558_2877980824822183944_n.jpg?oh=a3922d039b5be996ec56cdd05f14053d&oe=553AE0D4",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            },
            {
              "PostText": "Starting on my road trip. Can't wait! #BMWJoyRide",
              "PictureLoc": "https://scontent-a.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/10888643_10152913233001558_2877980824822183944_n.jpg?oh=a3922d039b5be996ec56cdd05f14053d&oe=553AE0D4",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            }
          ]
}
]
        """,

    """
        [
{
"EventID": 3,
"Timestamp": 100,
"PostData": [
            {
              "PostText": "Beautiful, warm, sunny view at Point Lobos State Reserve on my way to Big Sur. #BMWJoyRide",
              "PictureLoc": "https://scontent-a.xx.fbcdn.net/hphotos-xaf1/v/t1.0-9/10433831_10152913234081558_68780241031993015_n.jpg?oh=bda12765f27c4ef63974cc83b5813409&oe=5536D6B6",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            }
          ]
}
]
        """,

    """
        [
{
"EventID": 3,
"Timestamp": 100,
"PostData": [
            {
              "PostText": "Spending my first night at Big Sur Campground & Cabins. #BMWJoyRide",
              "PictureLoc": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xpa1/v/t1.0-9/10427676_10152913233196558_8295848653392814332_n.jpg?oh=91cb280aa6109796ccd40f60c8f54f20&oe=552D41D3&__gda__=1429856453_fb75c7a14398a0b630472771f916c8b1",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            }
          ]
}
]
        """,

    """
        [
{
"EventID": 3,
"Timestamp": 100,
"PostData": [
            {
              "PostText": "Take a look at this photo! #BMWJoyRide",
              "PictureLoc": "https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-xpa1/t31.0-8/p417x417/1512168_10152913233581558_6310571743314519856_o.jpg",
              "GPS": [37.8197, -122.4786],
              "PostingService": ["Twitter"]
            }
          ]
}
]
        """,
]

class Handler(BaseHTTPRequestHandler):
    all_candidate_posts = []

    def respond(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        global index

        self.respond(200)
        if self.path == '/joyride/tweets':
            if index < len(responses):
                message = responses[index]
                index += 1
                self.wfile.write(message)

        elif self.path == '/joyride/reset':
            index = 0

        return

    def do_POST(self):
        if self.path != '/joyride/event':
            self.respond(404)
            return
        try:
            length = int(self.headers.getheader('content-length'))
            data = json.loads(self.rfile.read(length))

            print 'Received data: ' + str(data)
            # Validate the incoming data
            result = ValidateData.validate(data, IncomingFormat)
            if result is not True:
                print 'Incoming request not formatted correctly: ', result
                self.respond(400)
                return

            # The APP wants all the candidate tweets.
            if data['EventID'] == 12:
                logging.info('Sending all candidate posts to App.')
                self.respond(200)
                self.all_candidate_posts = [] # Clear memory
                return


            # PreBroca returns a BrocaSendMessageFormat object
            logging.info('About to enter PreBroca.')
            candidate_posts = PreBroca.process(data)
            logging.info('Left PreBroca.')

            # PreBroca determined that the event was not tweetable.
            if candidate_posts is None:
                logging.info('Event not tweetable.')
                return

            if not ValidateData.validate(candidate_posts, OutgoingFormat):
                logging.info('Outgoing message not formatted correctly.')
                return

            # Store the candidate posts.
            logging.info('Saving %i candidate posts to global memory',
                         len(candidate_posts['PostData']))
            self.all_candidate_posts.append(candidate_posts)

            # send some response back
            self.respond(200)

        except Exception, e:
            print "Exception while receiving message: " + traceback.format_exc()
            self.respond(500)
            self.wfile.write("Data: " + str(data))
            self.wfile.write("Exception while receiving message: " + traceback.format_exc())
            return

if __name__ == "__main__":
  server = HTTPServer(('', 13373), Handler)
  server.serve_forever()

