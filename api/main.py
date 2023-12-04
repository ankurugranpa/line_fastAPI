from typing import Union

from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
# from fastapi import BaseModel


from api.routers import gpt
from api.routers import line


app = FastAPI(title="linebot-sample", description="connect scratch")
app.include_router(gpt.router)
app.include_router(line.router)

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

# Root
@app.get("/")
def root():
    return {"title": app.title, "description": app.description}


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item):
    print(item)
    return item
