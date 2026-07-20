from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi import HTTPException
load_dotenv()
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
async def call_llm(messages: list[dict]) -> str:
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API error: {str(e)}")