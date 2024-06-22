import sqlite3
import os
import pandas as pd
from flask import Flask, request, abort
from backend.build import *

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, DatetimePickerTemplateAction, PostbackEvent,
    PostbackTemplateAction, MessageAction, QuickReply, QuickReplyButton
)


app = Flask(__name__)

channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

create_table()

# 所有從line來的事件都會先經過此，再轉為下方的handler做進一步的處理
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# handler在收到事件後，會根據定義的行為做相對應的處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_input = event.message.text
    print(event.reply_token)
    if message_input == 'test':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='test'))
    elif message_input == 'music':
        jazz = get_data('爵士')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=jazz))


# 當py檔案被直接執行時，__name__變數會是__main__，因此當此條件成立時，代表程式被當作主程式執行，而不是被當作模組引用。
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=5000)