# reference: https://github.com/mdarvanaghi/CSGO-GSI/blob/master/gsi_server.py

from http.server import BaseHTTPRequestHandler, HTTPServer

class GSIServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int], RequestHandler: BaseHTTPRequestHandler, token: str = None):
        super().__init__(server_address, RequestHandler)
        self.token = token

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        print("------")
        print(body)


if __name__ == "__main__":
    server = GSIServer(("127.0.0.1", 5996), RequestHandler, "42069")
    server.serve_forever()
    server.server_close()