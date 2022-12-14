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
    
    def do_POST(self):

        print(self.path)
        parser = urlparse(self.path)
        self.path = parser.path
        response = {}
        content_length = self.headers['Content-Length']
        if content_length is not None:
            post_data = json.loads(self.rfile.read(int(content_length)).decode())
            if post_data != None:
                
                str = post_data.get("str")
                num1 = post_data.get("num1")
                num2 = post_data.get("num2")
                print(str)
                print(num1)
                print(num2)
                if str != None:
                    response["lowercase"] = 0 
                    response["uppercase"] = 0
                    response["digits"] = 0
                    response["special"] = 0

                    response["lowercase"] = sum(1 for c in str if c.islower())
                    response["uppercase"] = sum(1 for c in str if c.isupper())
                    response["digits"] = sum(1 for c in str if c.isnumeric())
                    response["special"] = len(str) - response["lowercase"] - response["uppercase"] - response["digits"]
                    
                if num1 != None and num2 != None:
                    num1 = int(num1)
                    num2 = int(num2)
                    response["sum"] = 0 
                    response["sub"] = 0
                    response["mul"] = 0
                    response["div"] = 0
                    response["mod"] = 0

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
            super().do_POST()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
