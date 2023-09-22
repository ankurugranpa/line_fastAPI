import os

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
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
from starlette.exceptions import HTTPException

# lineボット用の設定
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANEL_API_KEY')
USER_ID = os.environ.get('LINE_USER_ID')
CHANNEL_SECLET = os.environ.get('LINE_CANNEL_SECLET')

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECLET)


app = FastAPI(title="linebot-sample", description="connect scratch")


# Root
@app.get("/")
def root():
    return {"title": app.title, "description": app.description}


# Line Webhook
@app.post("/callback")
async def callback(request: Request, x_line_signature=Header(None)):

    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text = event.message.text
        if text == "ちんちん":
            text = "同じです"
        else:
            text = "違います"
        # print(event)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                # messages=[TextMessage(text=event.message.text)]
                messages=[TextMessage(text=text)]
            )
        )
