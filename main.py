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
    if '登録' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録したいのは何人？')
        )
    elif '人' in event.message.text:
        pattern=r'([0-9]*)'
        num_of_members = re.match(pattern,event.message.text)
        num_of_members = int(num_of_members[0])
        global member_names
        member_names = []
        for i in range(0, num_of_members):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(num_of_members - 1) + '人目の名前は？')
            )
            @handler.add(MessageEvent, message=TextMessage)
            def handle_message(event):
                member_names.append(event.message.text)

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='「' + event.message.text + '」って何？')
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
