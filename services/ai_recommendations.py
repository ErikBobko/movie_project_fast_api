import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from services.recommendations import get_recommendations

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

def get_ai_recommendations(prompt: str):
    filters = parse_user_prompt(prompt)

    recommendations = get_recommendations(
        genre=filters.get("genre"),
        min_rating=filters.get("min_rating") or 0,
        year_from=filters.get("year_from"),
        actor=filters.get("actor"),
        limit=10,
    )

    return {
        "prompt": prompt,
        "filters": filters,
        "recommendations": recommendations,
    }