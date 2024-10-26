from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import glob

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()  
        with open("./www/submit/index2.html", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        # Content-Lengthヘッダーからデータサイズを取得
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 送信されたデータを解析
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        name = parsed_data.get('ikey', [''])[0]
        age = parsed_data.get('ibody', [''])[0]

        # 解析結果を表示
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"<html><body><h2>受信データ</h2><p>名前: {name}</p><p>年齢: {age}</p></body></html>"
        self.wfile.write(response.encode('utf-8'))

# サーバー設定
port = 80
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"サーバーを起動しました。http://127.0.0.1:{port}")
files = glob.glob("*")
for file in files:
    print(file)
httpd.serve_forever()
