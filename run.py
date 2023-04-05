# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
import os
from dotenv import load_dotenv
load_dotenv()
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_SESRET = os.getenv("LINE_SESRET")

app = Flask(__name__)

@app.route("/api", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(LINE_TOKEN)
        handler = WebhookHandler(LINE_SESRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
        return 'OK'
    except:
        print('error')
        return 'XX'
@app.route("/test", methods=['GET'])
def test():
    return 'OKT3'

if __name__ == "__main__":
    # run_with_ngrok(app)
    # app.run()
    pass