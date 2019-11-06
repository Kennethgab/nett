
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO



class webmHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is a POST request\n')
        response.write(b'Received: \n')
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 8000), webmHTTPRequestHandler)
httpd.serve_forever()
