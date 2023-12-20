from enum import Enum

from pydantic import  BaseModel, Field
from typing import Optional, Union

class TypeName(Enum):
    audio = "audio"
    video = "video"
    image = "image"



class BlobBase(BaseModel):
    type: TypeName = Field(description="Content Type", example="audio")


class GetBlobUrl(BlobBase):
    base64_binary: str = Field(description="Base64 binary")


class GetBlobUrlResponse(BlobBase):
    url: str = Field(description="Content URL")