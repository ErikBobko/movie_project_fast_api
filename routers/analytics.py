from fastapi import APIRouter

from services.analytics import get_top_rated

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/top-rated")
def top_rated():
    return get_top_rated()