
import inspect
import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from services.recommendations import get_recommendations


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


def _safe_json_loads(text: str) -> Any:
    """
    Parse a JSON response and tolerate accidental Markdown code fences.
    """
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```")
        cleaned = cleaned.removesuffix("```").strip()

    return json.loads(cleaned)


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

    parsed = _safe_json_loads(response.output_text)

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


def _call_recommendation_service(filters: dict, limit: int) -> list:
    """
    Call services.recommendations.get_recommendations while remaining
    compatible with the current service function.

    If the service does not yet support exact year/year_to parameters,
    year is temporarily passed as year_from and results are then filtered
    exactly in Python.
    """
    signature = inspect.signature(get_recommendations)
    supported_parameters = set(signature.parameters)

    kwargs = {
        "genre": filters.get("genre"),
        "min_rating": filters.get("min_rating") or 0,
        "actor": filters.get("actor"),
        "limit": limit,
    }

    exact_year = filters.get("year")
    year_from = filters.get("year_from")
    year_to = filters.get("year_to")

    if "year" in supported_parameters:
        kwargs["year"] = exact_year
    elif "year_from" in supported_parameters:
        # Fetch candidates from the exact year onward, then post-filter.
        kwargs["year_from"] = exact_year if exact_year is not None else year_from

    if "year_from" in supported_parameters and "year_from" not in kwargs:
        kwargs["year_from"] = year_from

    if "year_to" in supported_parameters:
        kwargs["year_to"] = year_to

    # Remove arguments unsupported by the current service implementation.
    kwargs = {
        key: value
        for key, value in kwargs.items()
        if key in supported_parameters
    }

    recommendations = get_recommendations(**kwargs) or []

    if not isinstance(recommendations, list):
        raise TypeError("get_recommendations() must return a list.")

    return recommendations


def _post_filter_recommendations(
    recommendations: list,
    filters: dict,
    limit: int,
) -> list:
    """
    Enforce year and rating filters once more in Python.

    This prevents a broad database query or fallback from returning a movie
    that does not satisfy the user's requested year.
    """
    exact_year = filters.get("year")
    year_from = filters.get("year_from")
    year_to = filters.get("year_to")
    min_rating = filters.get("min_rating") or 0

    filtered = []

    for movie in recommendations:
        movie_year = movie.get("year")
        movie_rating = movie.get("rating")

        try:
            movie_year = int(movie_year) if movie_year is not None else None
        except (TypeError, ValueError):
            movie_year = None

        try:
            movie_rating = (
                float(movie_rating)
                if movie_rating is not None
                else 0
            )
        except (TypeError, ValueError):
            movie_rating = 0

        if exact_year is not None and movie_year != exact_year:
            continue

        if year_from is not None:
            if movie_year is None or movie_year < year_from:
                continue

        if year_to is not None:
            if movie_year is None or movie_year > year_to:
                continue

        if movie_rating < min_rating:
            continue

        filtered.append(movie)

        if len(filtered) >= limit:
            break

    return filtered


def _actor_names_from_movie(movie: dict) -> list[str]:
    """
    Read actor names from several common result formats.
    """
    raw_actors = (
        movie.get("actors")
        or movie.get("cast")
        or movie.get("actor_names")
        or []
    )

    names = []

    if isinstance(raw_actors, str):
        return [
            name.strip()
            for name in raw_actors.split(",")
            if name.strip()
        ]

    if not isinstance(raw_actors, list):
        return names

    for actor in raw_actors:
        if isinstance(actor, str):
            name = actor.strip()
        elif isinstance(actor, dict):
            name = str(actor.get("name") or "").strip()
        else:
            name = ""

        if name:
            names.append(name)

    return names


def _build_verified_movie_data(movie: dict, filters: dict) -> dict:
    """
    Prepare only verified data for the explanation model.
    """
    actor_names = _actor_names_from_movie(movie)
    requested_actor = filters.get("actor")

    actor_match = None

    if requested_actor and actor_names:
        requested_actor_lower = requested_actor.casefold()
        actor_match = any(
            requested_actor_lower == actor_name.casefold()
            for actor_name in actor_names
        )
    elif requested_actor:
        # The recommendation service already filtered by this actor, but the
        # returned record does not contain a cast list. Do not let the model
        # guess that the actor is absent.
        actor_match = True

    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "year": movie.get("year"),
        "rating": movie.get("rating"),
        "category": movie.get("category"),
        "overview": movie.get("overview"),
        "actors": actor_names,
        "requested_actor": requested_actor,
        "requested_actor_match": actor_match,
    }


def explain_recommendations(
    prompt: str,
    recommendations: list,
    filters: dict,
) -> list:
    """
    Generate short explanations without allowing the model to contradict
    verified database filters.
    """
    if not recommendations:
        return []

    movies_for_ai = [
        _build_verified_movie_data(movie, filters)
        for movie in recommendations[:5]
    ]

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
You are a movie recommendation assistant.

Original user request:
{prompt}

Parsed filters:
{json.dumps(filters, ensure_ascii=False)}

Verified movie data from my database:
{json.dumps(movies_for_ai, ensure_ascii=False)}

Write one short recommendation reason for each movie.

Rules:
- Use only the verified data provided above.
- Do not invent movies, actors, years, ratings, genres, or plot details.
- "requested_actor_match": true means the requested actor was matched by
  the database filter. Never say that this actor is absent.
- If "actors" is empty, it means the cast list was not included in the
  returned record. It does not mean that the requested actor is absent.
- Never infer actor absence from the overview.
- Every returned movie already satisfies the enforced year and rating filters.
- Keep each reason short and natural.
- Return only valid JSON and no Markdown.

Required format:
[
  {{
    "id": 123,
    "reason": "Short reason why this movie matches the request."
  }}
]
"""
    )

    result = _safe_json_loads(response.output_text)

    if not isinstance(result, list):
        raise ValueError("AI explanation response must be a JSON list.")

    valid_ids = {
        movie.get("id")
        for movie in recommendations
    }

    cleaned = []

    for item in result:
        if not isinstance(item, dict):
            continue

        movie_id = item.get("id")
        reason = item.get("reason")

        if movie_id not in valid_ids:
            continue

        if not isinstance(reason, str) or not reason.strip():
            continue

        cleaned.append({
            "id": movie_id,
            "reason": reason.strip(),
        })

    return cleaned


def get_ai_recommendations(prompt: str) -> dict:
    """
    Main public function used by the API or Streamlit application.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "prompt": prompt,
            "filters": {},
            "recommendations": [],
            "message": "Please enter a movie request.",
        }

    filters = normalize_filters(parse_user_prompt(prompt.strip()))

    print("AI filters:", filters)

    recommendations = get_recommendations(
        genre=filters.get("genre"),
        min_rating=filters.get("min_rating") or 0,
        year=filters.get("year"),
        year_from=filters.get("year_from"),
        year_to=filters.get("year_to"),
        actor=filters.get("actor"),
        sort_by=filters.get("sort_by"),
        sort_order=filters.get("sort_order"),
        limit=5,
    )
    if not recommendations:
        return {
            "prompt": prompt,
            "filters": filters,
            "recommendations": [],
            "message": (
                "No movie in the database matches all requested filters."
            ),
        }

    explanations = explain_recommendations(
        prompt=prompt,
        recommendations=recommendations,
        filters=filters,
    )

    explanation_map = {
        item["id"]: item["reason"]
        for item in explanations
    }

    for movie in recommendations:
        movie["ai_reason"] = explanation_map.get(
            movie.get("id"),
            "This movie matches the selected database filters.",
        )

    return {
        "prompt": prompt,
        "filters": filters,
        "recommendations": recommendations,
        "message": None,
    }