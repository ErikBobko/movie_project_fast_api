from fastapi import FastAPI

from routers.movies import router as movies_router
from routers.actors import router as actors_router
from routers.analytics import router as analytics_router
from routers.recommendations import router as recommendations_router
from routers.sync import router as sync_router
from routers.ai import router as ai_router
from routers.similar_movies import router as similar_movies_router


app = FastAPI(title="Movie Analytics API",description="API for movie analytics and recommendations",version="1.0.0")
app.include_router(movies_router)
app.include_router(actors_router)
app.include_router(analytics_router)
app.include_router(recommendations_router)
app.include_router(sync_router)
app.include_router(ai_router)
app.include_router(similar_movies_router)


@app.get("/", tags=["System"])
def root():
    return {"message": "Movie API is running"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}