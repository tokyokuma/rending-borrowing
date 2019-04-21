# インポートするライブラリ
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
import os
import re

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
global rending
global borrowing
global sum
lending = 0
borrowing = 0
sum = 0

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
    pattern=r'([0-9]*)'
    if '貸した' in event.message.text:
        rending_temp = re.findall(pattern,event.message.text)
        rending = int(rending_temp)
        sum = sum + rendig
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='計' + str(sum) + 'です')
        )
    elif '借りた' in event.message.text:
        borrowing_temp = re.findall(pattern,event.message.text)
        borrowing = int(borrowing_temp)
        sum = sum - borrowing
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='計' + str(sum) + 'です')
        )

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='「' + event.message.text + '」って何？')
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
