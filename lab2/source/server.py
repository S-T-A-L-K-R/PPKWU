#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import urlparse

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):

        print(self.path)
        if self.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            
            query = urlparse(self.path).query
            if query != '':
                query_components = dict(qc.split("=") for qc in query.split("&"))
                cmd = query_components["cmd"]
                print(cmd)
                if cmd == "time":
                    now = dt.now(pytz.timezone("Europe/Warsaw"))
                    s = now.strftime("%H:%M:%S") + "\n"
                    t = s.encode() 
                    self.wfile.write(t)
                elif cmd == "rev":
                    pass

            else:
                self.wfile.write(b"Hello World!\n")
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
