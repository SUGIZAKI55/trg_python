from http.server import BaseHTTPRequestHandler, HTTPServer

# デコレーターの定義
def admin_only(func):
    def wrapper(handler):
        if handler.path == '/admin':
            print("Admin route detected!")
            return func(handler)
        else:
            handler.send_response(403)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(b"403 Forbidden: Admins only!")
    return wrapper

class MyHandler(BaseHTTPRequestHandler):
    @admin_only
    def handle_admin(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Welcome to the Admin Page")
    
    def do_GET(self):
        if self.path == '/admin':
            self.handle_admin()  # /adminでデコレーターが適用される
        else:
            self.handle_default()

    def handle_default(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Page ga ugokimasita")

# https://chatgpt.com/share/8c79d074-d081-4aff-b974-d9b9a14e190d

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8080), MyHandler)
    print("Server started at http://localhost:8080")
    server.serve_forever()