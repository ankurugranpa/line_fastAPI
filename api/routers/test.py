import os
from dotenv import load_dotenv
from openai import OpenAI
import openai

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def call_gpt(prompt, question, lang="\n日本語で返答してください"):
    """
    access to openAI chat gpt
    Args:
        prompt(str):chat gpt system prompt
        question(str):chat gpt user query
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
print(call_gpt("あなたは岸田文雄です", "あなたは誰?"))