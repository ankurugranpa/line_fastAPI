import os
import requests
import  pprint
import asyncio

# from api.routers import line

from linebot import LineBotApi
from linebot.models import TextSendMessage
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
        PushMessageRequest
        )

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
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

def geturl_test():
    # url = "http://localhost:8001/"
    # url = "https://official-joke-api.appspot.com/jokes/random"
    # url = "http://api.open-notify.org/iss-now.json"
    # url = "https://jaguar-curious-conversely.ngrok-free.app/"
    url = "https://a11f-216-171-126-102.ngrok-free.app/"
    r = requests.get(url)
    print(r.json())



@router.post("/send_line/", response_model=line_schema.LineSendTextResponse)
async def send_message(line_body: line_schema.LineSendText):
    # print(message)
    # text = message.message
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    # line_bot_api.push_message(USER_ID, TextSendMessage(text=text))
    line_bot_api.push_message(line_body.user_id, TextSendMessage(text=line_body.message))
    return line_schema.LineSendTextResponse(status=200, **line_body.dict())


@router.post("/line_callback")
async def callback(request: Request, x_line_signature=Header(None)):

    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"


# async def line_get(line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)):




@handler.add(MessageEvent, message=TextMessageContent)
# def line_get(line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)):
def line_get(event):
    # , line_body: line_schema.LineGetMessage, db:AsyncSession =Depends(get_db)):
    # db : AsyncSession =Depends(get_db)
    # line_body: line_schema.LineGetMessage

    # geturl_test()
    with ApiClient(configuration) as api_client:
        ip = api_client.configuration
        # print(message)
        print(type(event))
        user_id = event.to_dict()['source']['userId']
        message = event.message.text

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,

                # reply_token=MessageEvent.reply_token,
                # messages=[TextMessage(text=event.message.text)]
                messages=[TextMessage(text="受信しました")]
            )
        )
    url = "https://a11f-216-171-126-102.ngrok-free.app/line-db/test"
    data ={"user_id": user_id,
        "message": message}
    r_post = requests.post(url, json=data)

    # return test
    # return  test()
    print(event)
    # return  geturl_test()
    # return  print("test")

    # await line_crud.add_message(AsyncSession =Depends(get_db),line_schema.LineGetMessage.message=message, line_schema.LineGetMessage.user_id=user_id)

    # return line_crud.add_message(Depends(get_db), test)
    # return set_db(line_body)






# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         # ip = api_client.configuration.
#         # print(event['source']['userId'])
#         # pprint(event['source']['userId'])
#         print(event.to_dict()['source']['userId'])
# 
# 
#         line_bot_api = MessagingApi(api_client)
#         # print(event.message)
#         text = event.message.text
#         if text == "あいうえお":
#             text = "同じです?"
#         else:
#             text = "違います"
#         # print(event)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 # messages=[TextMessage(text=event.message.text)]
#                 messages=[TextMessage(text=text)]
#             )
#         )
