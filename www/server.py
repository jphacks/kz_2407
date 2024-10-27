from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()  
        with open("./www/submit.html", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        # Content-Lengthヘッダーからデータサイズを取得
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 送信されたデータを解析
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        ibody = parsed_data.get('ibody', [''])[0]

        # 解析結果を表示
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"<html><body><h2>recv.data</h2><p>data: {ibody}</p></body></html>"
        self.wfile.write(response.encode('utf-8'))

# サーバー設定
port = 80
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Server is ready! on http://127.0.0.1:{port}")

httpd.serve_forever()