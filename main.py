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
cursor = con.cursor()

sql = "CREATE TABLE rent_borrow(date, id, rentborrow, amount, use);"
cursor.execute(sql)
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
    rent = 0
    borrow = 1
    use = event.message.text

    if '貸した' in event.message.text:
        rending_temp = re.findall(pattern,event.message.text)
        rending = int(rending_temp[0])
        cursor.execute(p, (date, profile.user_id, rent, rending, use))
        con.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='貸したのですね、了解です')
        )

    elif '借りた' in event.message.text:
        borrowing_temp = re.findall(pattern,event.message.text)
        borrowing = int(borrowing_temp[0]) * (-1)
        cursor.execute(p, (date, profile.user_id, borrow, borrowing, use))
        con.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='借りたのですね、了解です')
        )

    elif '状況' in event.message.text:
        cursor.execute('SELECT * FROM rent_borrow')
        sum = 0
        for row in cursor:
            if row[1] == profile.user_id:
                if row[2] == 0:
                    sum = sum + row[3]

                elif row[2] == 1:
                    sum = sum - row[3]

            else:
                if row[2] == 0:
                    sum = sum - row[3]

                elif row[2] == 1:
                    sum = sum + row[3]

        sum_str = str(sum)

        if sum > 0:
            situation = '円貸しています'
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=sum_str + situation)
            )

        elif sum < 0:
            situation = '円借りています'
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=sum_str + situation)
            )

        elif sum == 0:
            situation = '現状貸し借りは0円です'
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=situation)
            )

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='知らない言葉は使わないで')
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
