# インポートするライブラリ
import os
import re
import sqlite3
from datetime import datetime
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)



# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

con = sqlite3.connect('./rentborrow.db')
cur = con.cursor()

sql = "CREATE TABLE rent_borrow(date, id, rentborrow, amount, use);"
cur.execute(sql)
p = "INSERT INTO rent_borrow(date, id, rentborrow, amount, use) VALUES(?, ?, ?, ?, ?)"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    date = datetime.fromtimestamp(event.timestamp/1000.0)
    pattern=r'([0-9]*)'
    rent = '貸した'
    borrow = '借りた'
    use = ''

    if '貸した' in event.message.text:
        rending_temp = re.findall(pattern,event.message.text)
        rending = int(rending_temp[0])
        cursor.execute(p, (date, profile.user_id, rent, rending, use))
        con.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='貸した目的は？')
        )
    elif '借りた' in event.message.text:
        borrowing_temp = re.findall(pattern,event.message.text)
        borrowing = int(borrowing_temp[0])
        cursor.execute(p, (date, profile.user_id, borrow, borrowing, use))
        con.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='貸した目的は？')
        )

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='了解です')
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
