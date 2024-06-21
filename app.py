import sqlite3
import os
import pandas as pd
from flask import Flask, request, abort
from backend.build import *

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, DatetimePickerTemplateAction, PostbackEvent, PostbackTemplateAction,
    MessageAction, QuickReply, QuickReplyButton
)

app = Flask(__name__)

channel_access_token = os.environ.get('channel_access_token')
channel_secret = os.environ.get('channel_secret')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


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
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    message_input = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if message_input == 'test':
            line_bot_api.reply_message(event.reply_token,'test')
            # line_bot_api.reply_message_with_http_info(
            #     ReplyMessageRequest(
            #         reply_token=event.reply_token,
            #         messages=[TextMessage(text='test')],
            #     ))
        elif message_input == 'music':
            jazz = get_data('爵士')
            line_bot_api.reply_message(event.reply_token,jazz)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)