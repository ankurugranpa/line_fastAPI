from enum import Enum

from pydantic import  BaseModel, Field
from typing import Optional, Union


class BlobBase(BaseModel):
    type: str = Field(description="Content Type", example="audio, video, image")


class GetBlobUrl(BlobBase):
    base64_binary: str = Field(description="Base64 binary")


class GetBlobUrlResponse(BlobBase):
    url: str = Field(description="Content URL")