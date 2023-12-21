import os

import linebot.v3.webhooks
import requests
import  pprint
import asyncio

# from api.routers import line

from linebot import LineBotApi
from linebot.models import (
    AudioSendMessage,
    TextSendMessage,
    ImageSendMessage,
    VideoSendMessage
    )
from linebot.models import  ImageMessage
from linebot.models.messages import ContentProvider
from linebot.exceptions import LineBotApiError
# from fastapi import BaseModel

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
        Configuration,
        ApiClient,
        MessagingApi,
        ReplyMessageRequest,
        TextMessage,
        MessagingApiBlob,
        AudioMessage,
        PushMessageRequest
        )

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    AudioMessageContent,
    VideoMessageContent
)

from starlette.exceptions import HTTPException

from fastapi import APIRouter, Depends
from typing import Union
from sqlalchemy.ext.asyncio import  AsyncSession
from api.schemas import  line as   line_schema

from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
from dotenv import load_dotenv


router = APIRouter(
        prefix='/line',
        tags=['Line']
        )

# Setting Line Env
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANEL_API_KEY')
USER_ID = os.environ.get('LINE_USER_ID')
CHANNEL_SECLET = os.environ.get('LINE_CANNEL_SECLET')
DB_URL = os.environ.get('DB_BASE_URL')


configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECLET)


class Message(BaseModel):
    message: str


# Send Line Text Message
@router.post("/text", response_model=line_schema.LineSendResponse)
async def send_message(line_body: line_schema.LineSendText):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(line_body.user_id,
                              TextSendMessage(text=line_body.message))
    return line_schema.LineSendResponse(status=200, **line_body.dict())

# Send Line Audio Message
@router.post("/audio", response_model=line_schema.LineSendResponse)
async def send_audio(line_body: line_schema.LineSendAudio):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    # line_bot_api.push_message(line_body.user_id, TextSendMessage(text=line_body.message))
    line_bot_api.push_message(line_body.user_id,
                              AudioSendMessage(original_content_url=line_body.audio_url, duration=line_body.duration))
    return line_schema.LineSendResponse(status=200, **line_body.dict())

# Send Line Image Message
@router.post("/image", response_model=line_schema.LineSendResponse)
async def send_audio(line_body: line_schema.LineSendImage):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(line_body.user_id,
                                ImageSendMessage(original_content_url=line_body.image_url, preview_image_url=line_body.preview_image_url))
    return line_schema.LineSendResponse(status=200, **line_body.dict())


# Send Line Image Message
@router.post("/video", response_model=line_schema.LineSendResponse)
async def send_audio(line_body: line_schema.LineSendVideo):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(line_body.user_id,
                              VideoSendMessage(original_content_url=line_body.video_url, preview_image_url=line_body.preview_video_url))
    return line_schema.LineSendResponse(status=200, **line_body.dict())

@router.post("/callback")
async def callback(request: Request, x_line_signature=Header(None)):

    body = await request.body()
    # print(body)
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"

# async def line_get(line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)):

@handler.add(MessageEvent, message=TextMessageContent)
# def line_get(line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)):
def line_get(event):
    # geturl_test()
    with ApiClient(configuration) as api_client:
        user_id = event.to_dict()['source']['userId']
        message = event.message.text

        line_bot_api = MessagingApi(api_client)
        # line_bot_api.reply_message_with_http_info(
        # url = "https://ahahahaha.blob.core.windows.net/line-png-test/hare.mp3"
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    # ImageMessage(original_content_url=url, preview_image_url=url)
                    TextMessage(text="受信しました"),
                    # AudioMessage(original_content_url=url, duration=1900)
                ]
            )
        )
    url = f"{DB_URL}/line-db/test"

    data ={"user_id": user_id,
           "message": message}

    r_post = requests.post(url, json=data)
    print(event)

@handler.add(MessageEvent, message=AudioMessageContent)
def line_get_audio(event):
    print("Get Audio !!!!")
    with ApiClient(configuration) as api_client:
        api_instance = MessagingApiBlob(api_client)
        print(api_instance)

@handler.add(MessageEvent, message=ImageMessageContent)
def line_get_image(event):
    print(event)
    message_id = event.to_dict()['message']['id']
    print(message_id)

    print("Get Image !!!!")
    with ApiClient(configuration) as api_client:
        api_instance = MessagingApiBlob(api_client)
        print(api_instance)
