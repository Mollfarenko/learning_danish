from openai import OpenAI
from dotenv import load_dotenv
from .prompt import get_enrich_word_prompt
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_word(word: str) -> dict:
    prompt = get_enrich_word_prompt(word)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful language learning assistant. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    result = json.loads(response.choices[0].message.content)
    return result
