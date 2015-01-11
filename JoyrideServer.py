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

class Handler(BaseHTTPRequestHandler):
    all_candidate_posts = []

    def respond(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

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

            # send some response back
            self.respond(200)

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

        except Exception, e:
            print "Exception while receiving message: " + traceback.format_exc()
            self.respond(500)


if __name__ == "__main__":
  server = HTTPServer(('', 13373), Handler)
  server.serve_forever()

