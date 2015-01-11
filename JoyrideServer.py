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
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).strip())
            # Validate the incoming data
            result = ValidateData.validate(data, IncomingFormat)
            if result is not True:
                self.request.sendall(json.dumps({'failure': result}))
                return
            
            # PreBroca returns a BrocaSendMessageFormat object
            logging.info('About to enter PreBroca.')
            candidate_posts = PreBroca.process(data)
            logging.info('Left PreBroca.')
            
            result = ValidateData.validate(candidate_posts, OutgoingFormat)
            if result is not True:
                self.request.sendall(json.dumps({'failure': result}))
                return
            
            # send some response back
            self.request.sendall(json.dumps({'success': candidate_posts}))
            
        except Exception, e:
            print "Exception while receiving message: ", e

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = MyTCPServer(('127.0.0.1', 13373), MyTCPServerHandler)
    server.serve_forever()