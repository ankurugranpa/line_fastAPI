from typing import Optional, Union

from pydantic import BaseModel, Field


class LineBase(BaseModel):
    user_id: str
    channel_id: str
    channel_seclet: str


class LineSendText(LineBase):
    text_message: str


    """
    content: [str] = Field(None, example="自己紹介してください")
    prompt: Optional[str] = Field(default="You are a helpful assistant.")
    temperature: Optional[float] = Field(default=0.7)
    """


class LinePush(LineBase):
    pass


class LinePull(LineBase):
    pass
