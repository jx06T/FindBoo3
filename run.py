# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

app = Flask(__name__)

@app.route("/api", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi('/HRjFoiKvF6titv5x3wDFFB/t1OjrS7j8UGh8TK0gh1BbuPdhGKMBjm4yq84uOM2vc2aXMxqJnO5olfjZet+WEL0xO+iAVeBrycHMF7sPB23VgDXAoxcFxbYl9JoCR03+L8F1H/IeZn3kxuqEPnKuQdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('57d05fcee83d08744d3c34da8a970fc6')
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