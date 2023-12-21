from typing import Union

from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
# from fastapi import BaseModel


from api.routers import gpt
from api.routers import line
from api.routers import blob


app = FastAPI(title="ConnectionAPI for Scratch", description="Connect anything searvice")
app.include_router(gpt.router)
app.include_router(line.router)
app.include_router(blob.router)

origins = [
    "http://localhost:8601",
    "https://9ac3-216-171-126-102.ngrok-free.app"
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
