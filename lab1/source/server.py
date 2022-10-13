#!/usr/bin/env python3
import http.server
import socketserver
import os
import datetime
from datetime import datetime as dt
import pytz

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):

        print(self.path)
        # LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        now = dt.now(pytz.timezone("Europe/Warsaw"))
        # now = dt.now(LOCAL_TIMEZONE)
        s = now.strftime("%H:%M:%S") + "\n"
        t = s.encode() 
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()            
            self.wfile.write(b"Hello World!\n")
            self.wfile.write(t)
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
