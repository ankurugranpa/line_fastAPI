import os
from fastapi import APIRouter
import  api.schemas.gpt as gpt_schema
from openai import  OpenAI
from dotenv import load_dotenv
router = APIRouter()

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def call_gpt(question, prompt=None, lang="\n日本語で返答してください"):
    """
    access to openAI chat gpt
    Args:
        question(str):chat gpt user query
        prompt(str):chat gpt system prompt
        lang(str): set response language(default:ja)
    Returns:
        str: gpt returns text
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt+lang},
            {"role": "user", "content": question},
        ],
        temperature=0
    )
    return response.choices[0].message.content

@router.get("/task")
async def list_tasks():
    pass


@router.post("/gpt_ask", response_model=gpt_schema.GptAskResponse)
async def ask_gpt(gpt_body: gpt_schema.GptAsk):
    # return gpt_schema.GptAskResponse(response=call_gpt(gpt_body.prompt, gpt_body.content), **gpt_body.dict())
    # return gpt_schema.GptAskResponse(response=call_gpt("富士山について熱く語って", "あなたは博士です"), **gpt_body.dict())
    return gpt_schema.GptAskResponse(response=call_gpt(gpt_body.content, gpt_body.prompt), **gpt_body.dict())
