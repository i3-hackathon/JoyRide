#!/usr/bin/env python

import SocketServer
import json
import logging

import ValidateData
import PreBroca.Process as PreBroca
from MessageFormats.BrocaReceiveMessageFormat import EventMessageFormat as IncomingFormat
from MessageFormats.BrocaSendMessageFormat import EventMessageFormat as OutgoingFormat

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    all_candidate_posts = []
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).strip())
            # Validate the incoming data
            result = ValidateData.validate(data, IncomingFormat)
            if result is not True:
                logging.info('Incoming request not formatted correctly.')
                self.request.sendall(json.dumps({'failure': result}))
                return
            
            # The APP wants all the candidate tweets.
            if data['EventID'] == 12:
                logging.info('Sending all candidate posts to App.')
                self.request.sendall(json.dumps(self.all_candidate_posts))
                self.all_candidate_posts = [] # Clear memory
                return
            
            # send some response back
            self.request.sendall(json.dumps('success'))
            
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
            print "Exception while receiving message: ", e

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = MyTCPServer(('0.0.0.0', 13373), MyTCPServerHandler)
    server.serve_forever()