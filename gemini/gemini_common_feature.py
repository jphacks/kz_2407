# https://zenn.dev/peishim/articles/2e2e8408888f59
# https://gammasoft.jp/blog/stable-diffusion-with-diffusers-library/

# pip install google-generativeai python-dotenv
import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np

# pip install omegaconf pytorch_lightning xformers diffusers==0.12.1 transformers==4.19.2 ftfy accelerate
import torch
from diffusers import StableDiffusionPipeline


user = []
user.append("サッカー、ピアノ、ワンピース１０巻読んだ、釣り")
user.append("アニメ鑑賞、映画、野球、ラッパ")
user.append("本、映画、ギター、ドライブ、バスケ")

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")
# チャット履歴を初期化
chat = model.start_chat(history=[])

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

user_input3 = "これらから単語を一つ選んで、「*」,「Common」,「interests」,「hobbies」は選ばないで"
response3 = chat.send_message(user_input3)
response3 = response3.text
print(response3)


model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

# プロンプト
prompt = response3

# パイプラインの作成
pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)
pipe = pipe.to(device)

# パイプラインの実行
generator = torch.Generator(device).manual_seed(42) # seedを前回と同じ42にする
with torch.autocast("cuda"):
    image = pipe(prompt, guidance_scale=7.5, generator=generator).images[0]

# 生成した画像の保存
image.save("ai_img.png")
