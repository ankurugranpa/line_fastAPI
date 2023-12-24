from typing import Union
import  os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI, Request, Header
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
# from fastapi import BaseModel


from api.routers import gpt
from api.routers import line
from api.routers import blob
from dotenv import load_dotenv
load_dotenv()
SCRATCH_URL = os.environ.get('SCRATCH_URL')


app = FastAPI(title="ConnectionAPI for Scratch", description="Connect anything searvice")
app.include_router(gpt.router)
app.include_router(line.router)
app.include_router(blob.router)

origins = [
    "http://localhost:*",
    "https://*.ngrok-free.app",
    SCRATCH_URL,
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
    print(SCRATCH_URL)
    return {"title": app.title, "description": app.description}
