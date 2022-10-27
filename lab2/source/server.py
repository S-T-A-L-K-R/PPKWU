#!/usr/bin/env python3
import http.server
import socketserver
import os

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
            cmd = query_components.get("cmd")
            print(cmd)
            if cmd == "rev":
                str = query_components.get("str")
            
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            if cmd == "time":
                now = dt.now(pytz.timezone("Europe/Warsaw"))
                s = now.strftime("%H:%M:%S") + "\n"
                t = s.encode() 
                self.wfile.write(t)
            elif cmd == "rev":
                str = str[::-1]
                str = str.encode()
                self.wfile.write(str)
            else:
                self.wfile.write(b"Hello World!\n")
        else:
            super().do_GET()
    
# --- main ---

PORT = 4081

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
