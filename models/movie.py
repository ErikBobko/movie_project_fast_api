"""
MOVIE MODEL

Úloha:
- definuje dátovú štruktúru filmu v aplikácii
- validuje vstupné dáta pomocou Pydantic

Použitie:
- FastAPI request/response model
- reprezentácia filmu v aplikácii

Dôležité:
- neobsahuje business logiku
- nekomunikuje s databázou
- nekomunikuje s externými API
"""


from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    release_date: str | None = None
    tmdb_id: int | None = None
    rating: float | None = None
    original_language: str | None = None
    category: str | None = None
    popularity: float | None = None
    overview: str | None = None
    vote_count: int | None = None
    original_title: str | None = None
    year: int | None = None
