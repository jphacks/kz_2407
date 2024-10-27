# pip install google-generativeai python-dotenv
import os
from dotenv import load_dotenv
import google.generativeai as genai

# pip install omegaconf pytorch_lightning xformers diffusers==0.12.1 transformers==4.19.2 ftfy accelerate
import torch
from diffusers import StableDiffusionPipeline


# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")
# チャット履歴を初期化
chat = model.start_chat(history=[])

# ユーザーからの入力を受け取る
user_input = "サッカー、バスケ、散歩、ピアノ、アニメ、野球、サッカー"
user_input2 = "これらの共通点を見つけて英単語で１０個出して"

# チャットの応答
response = chat.send_message(user_input)
response2 = chat.send_message(user_input2)

print(response.text)
print(response2.text)



model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

# プロンプト
prompt = "サッカー"

# パイプラインの作成
pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)
pipe = pipe.to(device)

# パイプラインの実行
generator = torch.Generator(device).manual_seed(42) # seedを前回と同じ42にする
with torch.autocast("cuda"):
    image = pipe(prompt, guidance_scale=7.5, generator=generator).images[0]  

# 生成した画像の保存
image.save("ai_img.png")
