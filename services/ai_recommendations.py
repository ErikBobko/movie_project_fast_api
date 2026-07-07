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
  "actor": null,
  "mood": null,
  "theme": null,
  "reference_movie": null
}}

Rules:
- genre should match common movie genres like Action, Drama, Comedy, Thriller, Horror, Science Fiction, Fantasy, Animation, Adventure, Crime, Mystery, Romance, Family.
- mood can be dark, emotional, funny, scary, tense, romantic, inspiring, mysterious, relaxing.
- theme can be survival, space, revenge, friendship, war, crime, family, love, artificial intelligence, time travel.
- reference_movie is the movie title if user asks for something similar to a specific movie.
"""
    )

    text = response.output_text

    return json.loads(text)

GENRE_MAP = {
    "sci-fi": "Science Fiction",
    "science fiction": "Science Fiction",
    "scifi": "Science Fiction",

    "romcom": "Romance",
    "romantic": "Romance",

    "kids": "Family",
    "children": "Family",

    "action": "Action",
    "drama": "Drama",
    "comedy": "Comedy",
    "thriller": "Thriller",
    "horror": "Horror",
    "fantasy": "Fantasy",
    "animation": "Animation",
    "adventure": "Adventure",
    "crime": "Crime",
    "mystery": "Mystery",
}

def get_ai_recommendations(prompt: str):
    filters = parse_user_prompt(prompt)
    filters = normalize_filters(filters)

    print("AI filters:", filters)

    recommendations = get_recommendations(
        genre=filters.get("genre"),
        min_rating=filters.get("min_rating") or 0,
        year_from=filters.get("year_from"),
        actor=filters.get("actor"),
        limit=10,
    )

    explanations = explain_recommendations(prompt, recommendations)

    explanation_map = {
        item["id"]: item["reason"]
        for item in explanations
    }

    for movie in recommendations:
        movie["ai_reason"] = explanation_map.get(movie["id"])

    return {
        "prompt": prompt,
        "filters": filters,
        "recommendations": recommendations,
    }

def normalize_filters(filters: dict):
    genre = filters.get("genre")

    if genre:
        filters["genre"] = GENRE_MAP.get(
            genre.lower(),
            genre
        )

    mood = filters.get("mood")

    if mood:
        filters["mood"] = mood.lower()

    theme = filters.get("theme")

    if theme:
        filters["theme"] = theme.lower()

    return filters

def explain_recommendations(prompt: str, recommendations: list):
    if not recommendations:
        return []

    movies_for_ai = []

    for movie in recommendations[:5]:
        movies_for_ai.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "year": movie.get("year"),
            "rating": movie.get("rating"),
            "category": movie.get("category"),
            "overview": movie.get("overview"),
        })

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
You are a movie recommendation assistant.

User request:
{prompt}

Movies from my database:
{json.dumps(movies_for_ai, ensure_ascii=False)}

Task:
Write a short recommendation reason for each movie.

Rules:
- Use only the movies provided.
- Do not invent new movies.
- Return only JSON.
- Use this format:

[
  {{
    "id": 123,
    "reason": "Short reason why this movie matches the request."
  }}
]
"""
    )

    return json.loads(response.output_text)