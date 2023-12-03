from  typing import Optional, Union

from pydantic import  BaseModel, Field

class GptBase(BaseModel):
    content: Optional[str] = Field(None, example="自己紹介してください")
    prompt: Union[str,None]
class GptAsk(GptBase):
    lang: Optional[str] = Field(default="ja", example="ja")

class GptAskResponse(GptBase):
    response: str