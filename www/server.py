from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# https://zenn.dev/peishim/articles/2e2e8408888f59
import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
# https://gammasoft.jp/blog/stable-diffusion-with-diffusers-library/import torch
from diffusers import StableDiffusionPipeline

def gemini_setting():
    # .envファイルの読み込み
    load_dotenv()

    # API-KEYの設定
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-pro")
    # チャット履歴を初期化
    chat = model.start_chat(history=[])
    
    return chat

def conversation(chat, user):
    num = 0
    for hobby in user:
        num += 1
        user_input = str(num) + "人目の趣味は" + hobby
        response = chat.send_message(user_input)

    user_input2 = "彼らの趣味の共通点を英単語のみで言って"
    response2 = chat.send_message(user_input2)

    response2 = response2.text
    response2 = response2.split()
    #print(response2)

    user_input3 = "これらから単語を一つ選んで、選んだ単語のみ言って、「*」,「Common」,「interests」,「hobbies」は選ばないで"
    response3 = chat.send_message(user_input3)

    return response3.text

def ai_img(prompt):
    
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda"

    # パイプラインの作成
    pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)
    pipe = pipe.to(device)

    # パイプラインの実行
    generator = torch.Generator(device).manual_seed(42) # seedを前回と同じ42にする
    with torch.autocast("cuda"):
        image = pipe(prompt, guidance_scale=7.5, generator=generator).images[0]

    return image

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()  
        with open("./submit.html", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        # Content-Lengthヘッダーからデータサイズを取得
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 送信されたデータを解析
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        ibody = parsed_data.get('ibody', [''])[0]

        user = []
        user.append(ibody)

        chat = gemini_setting()
        response = conversation(chat, user)

        # 解析結果を表示
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"<html><head><meta charset='utf-8'/></head><body><h2>recv.data</h2><p>data: {response}</p></body></html>"
        self.wfile.write(response.encode('utf-8'))
        
        image = ai_img(response)

        # 生成した画像の保存
        image.save("ai_img.png")

# サーバー設定
port = 8081
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Server is ready! on http://127.0.0.1:{port}")

httpd.serve_forever()
