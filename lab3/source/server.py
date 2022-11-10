#!/usr/bin/env python3
import http.server
import socketserver
import os
import json

from datetime import datetime as dt
from urllib.parse import urlparse
import pytz

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
    
        print(self.path)
        parser = urlparse(self.path)
        self.path = parser.path
        query = parser.query
        cmd = ''
        if query != '':
            query_components = dict(qc.split("=") for qc in query.split("&"))
            str = query_components.get("str")
            print(str)
            
        response =  {"lowercase" : 0, 
                     "uppercase" : 0,
                     "digits" : 0,
                     "special" : 0}
        response["lowercase"] = sum(1 for c in str if c.islower())
        response["uppercase"] = sum(1 for c in str if c.isupper())
        response["digits"] = sum(1 for c in str if c.isnumeric())
        response["special"] = len(str) - response["lowercase"] - response["uppercase"] - response["digits"]
        
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            # self.wfile.write(b"Hello World!\n")
            self.wfile.write(json.dumps(response))
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
