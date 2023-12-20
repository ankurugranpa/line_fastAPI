from typing import Optional, Union

from pydantic import BaseModel, Field


class LineBase(BaseModel):
    user_id: str

class LineResponseBase(BaseModel):
    status: int


class LineSendText(LineBase):
    message: str

class LineSendAudio(LineBase):
    audio_url: str
    duration: int


class LineSendTextResponse(LineSendText):
    status: int


class LineSendAudioResponse(LineSendAudio):
    status: int

    """
    content: [str] = Field(None, example="自己紹介してください")
    prompt: Optional[str] = Field(default="You are a helpful assistant.")
    temperature: Optional[float] = Field(default=0.7)
    """
class LineGetMessage(LineBase):
    message: str
    class Config:
       model_config = True
