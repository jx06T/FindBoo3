# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import URIAction, TextSendMessage, MessageAction, TemplateSendMessage, CarouselTemplate,  CarouselColumn  # 載入 TextSendMessage 模組
import json
import os
from dotenv import load_dotenv
"""-----------------------------------------------"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
cookies = {
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0=%E5%88%A5%E4%BE%86%E7%84%A1%E6%81%99&t0=k&c0=and',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',

}
URL = "https://webpac.tphcc.gov.tw/webpac/search.cfm"


def search(keyword, times):
    params = {
        'm': 'ss',
        'k0': keyword,
        't0': 'k',
        'c0': 'and',
        "list_num": times*10,
    }
    response = requests.get(
        URL, params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = []
    i = 0
    for box in soup.find_all(class_="book"):
        if i < (times-1)*10:
            i += 1
            continue

        a = box.find("a")
        bigname = a.get("title")
        if len(bigname) > 40:
            name = bigname[0:37]+"..."
        else:
            name = bigname
        url = urljoin(URL, a.get("href").replace("¤", "&"))

        a = box.find_all("p")
        writer = a[1].text[3:]
        if len(writer) > 25:
            writer = writer[0:22]+"..."
        f = a[3].text[5:]
        if len(f) > 25:
            f = f[0:22]+"..."
        if a[min(4, len(a)-1)].text[0] != "I" or a[min(4, len(a)-1)].text[10:min(25, len(a[4].text)) == ""]:
            id = bigname+" "+writer
        else:
            id = name + " "+writer + " " + \
                a[4].text[10:min(25, len(a[4].text))]
        count = re.findall(r"\d+", a[len(a)-1].text)

        a = {"name": name, "url": url, "writer": writer,
             "count": count, "ISBN/ISSN": id, "from": f}
        titles.append(a)
        i += 1

    Blist = []
    for book in titles:
        C = CarouselColumn(
            title=book['name'],
            text="By "+book['writer']+"\n"+book["from"] +
            "\n"+book['count'][1]+"/"+book['count'][0],
            actions=[
                MessageAction(
                    label='查詢狀態',
                    text="$S "+str(book['ISBN/ISSN'])
                ),
                URIAction(
                    label='網頁連結',
                    uri=book["url"]
                )
            ]
        )
        Blist.append(C)
    return Blist


load_dotenv()
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_SESRET = os.getenv("LINE_SESRET")
LINE_MYID = os.getenv("LINE_MYID")
app = Flask(__name__)


@app.route("/api", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        line_bot_api = LineBotApi(LINE_TOKEN)
        handler = WebhookHandler(LINE_SESRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        name = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        if "$S " not in name:
            text_message = TextSendMessage(text=str(tk))          # 設定回傳同樣的訊息
            line_bot_api.reply_message(tk, text_message)

            msg = search(str(name), 1)
            line_bot_api.push_message(tk, TemplateSendMessage(
                alt_text='CarouselTemplate',
                template=CarouselTemplate(columns=msg)))
        else:
            text_message = TextSendMessage(text="開發中...")          # 設定回傳同樣的訊息
            line_bot_api.reply_message(tk, text_message)
    except:
        print("ww")
        pass

    return "ok"


@app.route("/test", methods=['GET'])
def test():
    return '05:16'


@app.route("/test/<name>", methods=['GET'])
def test2(name):
    line_bot_api = LineBotApi(LINE_TOKEN)
    msg = search(name, 1)
    line_bot_api.push_message(LINE_MYID, TemplateSendMessage(
        alt_text='CarouselTemplate',
        template=CarouselTemplate(columns=msg)))
    return 'send'


if __name__ == "__main__":
    # run_with_ngrok(app)
    app.run()
    pass
