from fastapi import APIRouter

from services.recommendations import get_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("")
def recommendations(
    genre: str | None = None,
    min_rating: float = 0,
    min_vote_count: int = 100,
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    actor: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    limit: int = 10,
):
    return get_recommendations(
        genre=genre,
        min_rating=min_rating,
        min_vote_count=min_vote_count,
        year=year,
        year_from=year_from,
        year_to=year_to,
        actor=actor,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
    )