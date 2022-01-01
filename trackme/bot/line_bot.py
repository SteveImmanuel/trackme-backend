from flask import Request
from typing import cast
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from trackme.contants import *

# initialize connector
api = LineBotApi(LINE_BOT_ACCESS_TOKEN)
handler = WebhookHandler(LINE_BOT_CHANNEL_SECRET)


def process_webhook(request: Request):
    signature = request.headers.get('X-Line-Signature')
    data = request.get_data(as_text=True)
    handler.handle(data, signature)


@handler.add(MessageEvent, message=TextMessage)
def echo(event: MessageEvent) -> None:
    message = cast(TextMessage, event.message)
    api.reply_message(event.reply_token, TextSendMessage(text=message.text))
