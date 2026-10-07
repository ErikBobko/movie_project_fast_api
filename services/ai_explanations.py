import json

from clients.openai_client import get_openai_client
from services.ai_utils import safe_json_loads


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

    client = get_openai_client()

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
- Write each recommendation reason in the same language as the user's request.
Required format:
[
  {{
    "id": 123,
    "reason": "Short reason why this movie matches the request."
  }}
]
"""
    )

    result = safe_json_loads(response.output_text)

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
