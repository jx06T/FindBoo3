from typing import Union
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import time
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   
import json

load_dotenv()

key = os.getenv("FAKE_VALUE")
app = FastAPI()


@app.post("/api")
async def MainApi(request: Request):
    json_data = await request.json()
    body = await request.body()
    print(json_data)
    try:
        line_bot_api = LineBotApi('1660832705')
        handler = WebhookHandler('57d05fcee83d08744d3c34da8a970fc6')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'


@app.get("/test")
def read_item():
    now = date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {"ya": now}
