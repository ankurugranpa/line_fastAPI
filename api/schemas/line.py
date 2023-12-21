from typing import Optional, Union

from pydantic import BaseModel, Field


class LineBase(BaseModel):
    user_id: str = Field(description="Line User Id")

class LineResponseBase(BaseModel):
    status: int = Field(description="callback status")


class LineSendText(LineBase):
    message: str = Field(description="Text Message @size: Max 5000word")

class LineSendAudio(LineBase):
    audio_url: str = Field(description="Audio Url @type: mp3, m4a @size Max200MB")
    duration: int = Field(description="Audio content length @type ms")

class LineSendImage(LineBase):
    image_url: str = Field(description="Image Url @type: jpeg, png @size: Max10MB")
    preview_image_url: str = Field(description="Preview Image URL @type: jpeg, png @size: Max1MB")

class LineSendVideo(LineBase):
    video_url: str = Field(description="Video URL @type: mp4 @size: Max200MB")
    preview_video_url: str = Field(description="Preview Video URL @type: jpeg, png @size: Max1MB")


class LineSendResponse(LineSendText):
    status: int


class LineGetMessage(LineBase):
    message: str
    class Config:
       model_config = True
