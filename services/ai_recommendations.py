import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def parse_user_prompt(prompt: str):
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Convert the movie request into JSON.

Return only JSON.

User request:
{prompt}

JSON format:
{{
  "genre": null,
  "min_rating": null,
  "year_from": null,
  "actor": null
}}
"""
    )

    text = response.output_text

    return json.loads(text)