# pip install omegaconf pytorch_lightning xformers diffusers==0.12.1 transformers==4.19.2 ftfy accelerate

import torch
from diffusers import StableDiffusionPipeline

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
