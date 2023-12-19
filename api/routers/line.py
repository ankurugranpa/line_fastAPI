import os

import linebot.v3.webhooks
import requests
import  pprint
import asyncio

# from api.routers import line

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import ImageSendMessage
from linebot.models import AudioSendMessage
from linebot.models import  ImageMessage
from linebot.models import  AudioMessage
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
        PushMessageRequest
        )

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    AudioMessageContent
)

from starlette.exceptions import HTTPException

from fastapi import APIRouter, Depends
from typing import Union
from sqlalchemy.ext.asyncio import  AsyncSession
import  api.cruds.line as line_crud
from api.db import  get_db
from api.schemas import  line as   line_schema

from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
from dotenv import load_dotenv


router = APIRouter()

# Setting Line Env
load_dotenv()
# test vierv
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANEL_API_KEY')
USER_ID = os.environ.get('LINE_USER_ID')
CHANNEL_SECLET = os.environ.get('LINE_CANNEL_SECLET')


configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECLET)


class Message(BaseModel):
    message: str

async def set_db(
        line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)
        ):
    return line_crud.add_message(db, line_body)
def line_get2(line_body: line_schema.LineGetMessage):
    return  set_db(line_body)




@router.post("/send_line/", response_model=line_schema.LineSendTextResponse)
async def send_message(line_body: line_schema.LineSendText):
    # print(message)
    # text = message.message
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    # line_bot_api.push_message(USER_ID, TextSendMessage(text=text))
    # line_bot_api.push_message(line_body.user_id, TextSendMessage(text=line_body.message))
    # ContentProvider("https://ahahahaha.blob.core.windows.net/line-png-test/hare.mp3")
    #  audio = ContentProvider(type="audio",  original_content_url="https://www.ne.jp/asahi/music/myuu/wave/menuettm.mp3")

    line_bot_api.push_message(to=line_body.user_id, messages=AudioSendMessage(content_provider="https://ahahahaha.blob.core.windows.net/line-png-test/hare.mp3", duration=1900))
    return line_schema.LineSendTextResponse(status=200, **line_body.dict())


@router.post("/line_callback")
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
async def line_get(event):
    # geturl_test()
    with ApiClient(configuration) as api_client:
        ip = api_client.configuration
        # print(message)
        # print(type(event))
        user_id = event.to_dict()['source']['userId']
        message = event.message.text

        line_bot_api = MessagingApi(api_client)
        ulr_imag="https://ahahahaha.blob.core.windows.net/line-png-test/zennketugou2.png"
        # line_bot_api.reply_message_with_http_info(
        url = "https://ahahahaha.blob.core.windows.net/line-png-test/hare.mp3"
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    # ImageMessage(original_content_url=url, preview_image_url=url)
                    # TextMessage(text="受信しました"),
                    AudioMessage(original_content_url=url, duration=1900)
                ]
            )
        )
        # message_test=ImageMessage(original_content_url=ulr_imag, preview_image_url=ulr_imag)
        # line_bot_api.reply_message(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         # me
        #         message=[ImageMessage(original_content_url=ulr_imag, preview_image_url=ulr_imag)]
        #         # messages=[message_test]
        #         # reply_token=MessageEvent.reply_token,
        #         # messages=[TextMessage(text=event.message.text)]
        #         # messages=[TextMessage(text="受信しました")]
        #         # messags=[Audi]
        #         # ImageSendMessage(original_content_url=ulr_imag, preview_image_url=ulr_imag)
        #         # messages=[AudioMessage(content_provider="https://ahahahaha.blob.core.windows.net/line-png-test/hare.mp3", duration=137000)]
        #     )
        # )
    url = "https://9ac3-216-171-126-102.ngrok-free.app/line-db/test"
    # data ={"user_id": user_id,
      #  "message": message}
    # r_post = requests.post(url, json=data)
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
