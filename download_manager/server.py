import http.server
import socketserver
import json
import threading
from PyQt6.QtCore import QObject, pyqtSignal

class DownloadRequestHandler(http.server.SimpleHTTPRequestHandler):
    # This is a class attribute that will be set from the outside
    url_receiver = None

    def do_POST(self):
        if self.path == '/add_download':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                url = data.get('url')
                if url and self.url_receiver:
                    self.url_receiver.new_url.emit(url)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'OK')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Bad Request: URL not found or receiver not set')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

class UrlReceiver(QObject):
    new_url = pyqtSignal(str)

class ServerThread(threading.Thread):
    def __init__(self, url_receiver, port=8080):
        super().__init__()
        self.port = port
        self.handler = DownloadRequestHandler
        self.handler.url_receiver = url_receiver
        self.httpd = None

    def run(self):
        try:
            with socketserver.TCPServer(("", self.port), self.handler) as self.httpd:
                print(f"Serving on port {self.port}")
                self.httpd.serve_forever()
        except Exception as e:
            print(f"Server error: {e}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
