
from services.recommendations import get_recommendations
from services.ai_prompt_parser import (
    parse_user_prompt,
    normalize_filters,
)
from services.ai_explanations import explain_recommendations


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