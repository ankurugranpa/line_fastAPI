import os
from fastapi import APIRouter
import  api.schemas.gpt as gpt_schema
from openai import  OpenAI
from dotenv import load_dotenv
router = APIRouter(
        prefix='/gpt',
        tags=['Gpt']
        )

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def call_gpt(question,
             prompt="You are a helpful assistant.",
             temperature=0.7,
             lang="\n日本語で返答してください"):
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
        temperature=temperature
    )
    return response.choices[0].message.content


@router.post("/ask", response_model=gpt_schema.GptAskResponse)
async def ask_gpt(gpt_body: gpt_schema.GptAsk):
    """
    Request Gpt respons
    """
    return gpt_schema.GptAskResponse(
            response=call_gpt(gpt_body.content,
                              gpt_body.prompt,
                              gpt_body.temperature),
            **gpt_body.dict()
            )
