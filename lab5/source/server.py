#!/usr/bin/env python3
import http.server
import socketserver
import os
import json

#print('source code for "http.server":', http.server.__file__)

from datetime import datetime as dt
from urllib.parse import urlparse
import pytz

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):

        print(self.path)
        parser = urlparse(self.path)
        self.path = parser.path
        query = parser.query
        cmd = ''
        if query != '':
            query_components = dict(qc.split("=") for qc in query.split("&"))
            num1 = int(query_components.get("num1"))
            num2 = int(query_components.get("num2"))
            str = query_components.get("str")
            print(num1)
            print(num2)
            print(str)
            
        response =  {"lowercase" : 0, 
                     "uppercase" : 0,
                     "digits" : 0,
                     "special" : 0}
        response["lowercase"] = sum(1 for c in str if c.islower())
        response["uppercase"] = sum(1 for c in str if c.isupper())
        response["digits"] = sum(1 for c in str if c.isnumeric())
        response["special"] = len(str) - response["lowercase"] - response["uppercase"] - response["digits"]
        
            
        response =  {"sum" : 0, 
                     "sub" : 0,
                     "mul" : 0,
                     "div" : 0,
                     "mod" : 0}

        response["sum"] = num1 + num2
        response["sub"] = num1 - num2
        response["mul"] = num1 * num2
        response["div"] = int(num1 / num2)
        response["mod"] = num1 % num2
        
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            # self.wfile.write(b"Hello World!\n")
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
