from clients.openai_client import get_openai_client
from services.ai_utils import safe_json_loads


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
    "romance": "Romance",
    "family": "Family",
}


def parse_user_prompt(prompt: str) -> dict:
    """
    Convert a natural-language movie request into normalized filters.

    year:
        Exact year, e.g. "film from 2020".

    year_from:
        Lower boundary, e.g. "from 2020 onward" or "after 2020".

    year_to:
        Upper boundary, e.g. "before 2020" or "up to 2020".
    """
    client = get_openai_client()

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Convert the user's movie request into JSON.

Return only valid JSON. Do not include Markdown.

User request:
{prompt}

Required JSON format:
{{
  "genre": null,
  "min_rating": null,
  "year": null,
  "year_from": null,
  "year_to": null,
  "actor": null,
  "sort_by": null,
  "sort_order": null,
  "mood": null,
  "theme": null,
  "reference_movie": null
}}

Rules:
- Use "year" when the user asks for one exact year.
  Example: "a movie from 2020" -> "year": 2020.
- Use "year_from" when the user asks for movies from a year onward.
  Example: "movies from 2020 onward" -> "year_from": 2020.
- For "after 2020", use "year_from": 2021.
- Use "year_to" when the user asks for movies up to or before a year.
  Example: "movies up to 2020" -> "year_to": 2020.
- For "before 2020", use "year_to": 2019.
- Do not put an exact-year request into "year_from".
- actor must contain only the actor's name.
- min_rating must be a number or null.
- genre should match common movie genres such as Action, Drama, Comedy,
  Thriller, Horror, Science Fiction, Fantasy, Animation, Adventure,
  Crime, Mystery, Romance, or Family.
- mood can be dark, emotional, funny, scary, tense, romantic,
  inspiring, mysterious, or relaxing.
- theme can be survival, space, revenge, friendship, war, crime,
  family, love, artificial intelligence, or time travel.
- reference_movie is the movie title when the user asks for something
  similar to a specific movie.
  - sort_by can be "rating", "popularity", "year", or null.
- sort_order can be "asc", "desc", or null.
- For "worst rated" or "lowest rated", use:
  "sort_by": "rating",
  "sort_order": "asc".
- For "best rated" or "highest rated", use:
  "sort_by": "rating",
  "sort_order": "desc".
- For "most popular", use:
  "sort_by": "popularity",
  "sort_order": "desc".
- For "oldest", use:
  "sort_by": "year",
  "sort_order": "asc".
- For "newest", use:
  "sort_by": "year",
  "sort_order": "desc".
"""
    )

    parsed = safe_json_loads(response.output_text)

    if not isinstance(parsed, dict):
        raise ValueError("AI parser did not return a JSON object.")

    return parsed



def normalize_filters(filters: dict) -> dict:
    """
    Normalize values returned by the AI parser.
    """
    normalized = dict(filters)

    genre = normalized.get("genre")
    if isinstance(genre, str) and genre.strip():
        normalized["genre"] = GENRE_MAP.get(
            genre.strip().lower(),
            genre.strip(),
        )

    actor = normalized.get("actor")
    if isinstance(actor, str):
        normalized["actor"] = actor.strip() or None

    for field in ("mood", "theme"):
        value = normalized.get(field)
        if isinstance(value, str):
            normalized[field] = value.strip().lower() or None

    for field in ("year", "year_from", "year_to"):
        value = normalized.get(field)
        if value in ("", None):
            normalized[field] = None
            continue

        try:
            normalized[field] = int(value)
        except (TypeError, ValueError):
            normalized[field] = None

    min_rating = normalized.get("min_rating")
    if min_rating in ("", None):
        normalized["min_rating"] = 0
    else:
        try:
            normalized["min_rating"] = float(min_rating)
        except (TypeError, ValueError):
            normalized["min_rating"] = 0

    return normalized
