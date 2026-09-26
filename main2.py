from fastapi import FastAPI

from routers.movies import router as movies_router
from routers.actors import router as actors_router


app = FastAPI(title="Movie Analytics API",description="API for movie analytics and recommendations",version="1.0.0")
app.include_router(movies_router)
app.include_router(actors_router)

@app.get("/", tags=["System"])
def root():
    return {"message": "Movie API is running"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}