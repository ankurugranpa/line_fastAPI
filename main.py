import os

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests


CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANEL_API_KEY')
USER_ID = os.environ.get('LINE_USER_ID')

app = FastAPI()


origins = [
    "http://localhost:8601",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def send_notify(message):
    url = "https://notify-api.line.me/api/notify"
    token = "Iz5Kax5Z8h5XrRCxFDbZVxsMMQAbrT1JIPiya37J0cT"
    headers = {"Authorization": "Bearer " + token}

    # message = 'message送信！'
    payload = {"message":  message}

    requests.post(url, headers=headers, params=payload)


def send_message(text):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    print("test")
    try:
        line_bot_api.push_message(USER_ID, TextSendMessage(text=text))
    except LineBotApiError as e:
        print(e.message)


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # send_notify(item_id)
    item = {"item_id": item_id}
    print("test")
    text = "これはline message apiを使用して送信しています。" + item_id
    send_message(text)
    # if q:
    #     item.update({"q": q})
    # if not short:
    #     item.update(
    #         {"description": "This is an amazing item that has a long description"}
    #     )
    return item
