import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from cimlibrary import CIMHandler
from io import BytesIO



class webmHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


    def do_POST(self):
        cim = CIMHandler()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
#        response.write(b'This is a POST request\n')
 #       response.write(b'Received: \n')
        parsed_data = json.loads(body)
        operation = parsed_data['method']
        classname = parsed_data['className']
        instancename = parsed_data['instanceName']
        rec_data = cim.send_req(operation,  className=classname, instanceName=instancename )
        self.wfile.write(bytes(rec_data,'utf-8'))
        self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8000), webmHTTPRequestHandler)
httpd.serve_forever()
