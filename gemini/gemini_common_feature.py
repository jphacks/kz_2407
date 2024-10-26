# pip install google-generativeai python-dotenv

import os
from dotenv import load_dotenv
import google.generativeai as genai

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
